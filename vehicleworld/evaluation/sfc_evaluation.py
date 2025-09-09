import argparse
import copy
import glob
import json
import statistics
import traceback
import sys
from agent_client import AgentClient
from eval_utils import read_tasks, extract_text, calculate_turn_result, compare_objects_values, get_current_world_dict, add_modules
sys.path.append('../')
from vehicleworld import *
from utils import save_json_file, execute
import logging
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed  # Changed to use ThreadPoolExecutor
from tqdm import tqdm

# Logging configuration
logging.basicConfig(
    level=logging.ERROR,
    format='[%(asctime)s] %(levelname)s in %(threadName)s: %(message)s'
)

def generate_plan_instruction():
    instruction = f"""
    You are an in-car AI assistant responsible for executing user requests. Based on the user's command, your first step is to generate a plan.
    **Example Task Flow**
    User:
    Navigate to the nearest gas station and turn up the navigation volume a bit.
    Assistant:
    The user wants to start navigation to the nearest gas station and slightly increase the navigation volume. To fulfill this request, I need to identify and operate the modules responsible for navigation and volume control. I will also check which APIs are available in these modules to carry out the required actions.
"""
    return instruction

def generate_state_instruction(sample=True):
    instruction = """
You are an intelligent vehicle AI assistant, your task is to help users analyze the vehicle system status to complete various tasks.

## Current System Status
1. The system will first provide you with the current status of the vehicle environment, including various information related to the task. You should fully understand the system status information and generate status modification code to complete the user-specified task.
2. After each code execution, the system status will be updated, and you need to determine whether the task has been completed or further operations are needed based on the return value of the code execution and the updated system status.
3. If the system status does not support executing the user's request, please refuse.

## Status Analysis Principles
When analyzing system status, please follow these principles:
1. Carefully check all available system modules and parameters
2. Understand the data types and value ranges of each field
3. Pay attention to the dependency relationships of status values, such as certain operations requiring specific sound channels
4. Prioritize using the ready-made data provided by the system, avoiding creating unnecessary new values
5. Ensure changes comply with system constraints

## Response Format
Your response should include the following parts:
1. Brief analysis of the user's question and code execution results
2. Code execution section (surrounded by ```python```, containing only status changes, do not include other code)
3. Do not generate other additional content
"""
    if sample:
        instruction += """
## Example Task Flow

### Example 1
User:
Play the video I've downloaded
Current system status:
vw = {
    "video": {
                "value": {
                    "current_video": {
                        "value": {
                            "video_id": {
                                "value": "dl_001",
                                "type": "str",
                                "description": "Unique identifier for video"
                            },
                            "title": {
                                "value": "Highway Safety Tutorial",
                                "type": "str",
                                "description": "Title of the video"
                            },
                            "description": {
                                "value": "Learn about best practices for highway driving and safety tips",
                                "type": "str",
                                "description": "Description of the video"
                            }
                            ...
                        },
                        "type": "VideoItem",
                        "description": "Currently selected video."
                    },
                    "downloaded_videos": {
                        "value": [
                            {
                                "video_id": {
                                    "value": "dl_001",
                                    "type": "str",
                                    "description": "Unique identifier for video"
                                },
                                "title": {
                                    "value": "City Night Drive",
                                    "type": "str",
                                    "description": "Title of the video"
                                },
                                "description": {
                                    "value": "Exploring the city streets at night with ambient lighting",
                                    "type": "str",
                                    "description": "Description of the video"
                                }
                                ...
                            },
                        ],
                        "type": "List[VideoItem]",
                        "description": "List of downloaded videos"
                    },
                    
                    
                },
                "description": "Video system",
                "type": "Video"
            }
}

Assistant:
The user needs to play a downloaded video, so I need to play the first video in the downloaded_videos list
```python
vw['video']['value']['current_video']['value'] = vw['video']['value']['downloaded_videos'][0]
```

### Example 2
User:
Turn up the volume a bit
Current system status:
vw = {
    "environment": {
                "value": {
                    "volume": {
                        "type": "int",
                        "value": 50,
                        "description": "Volume level (0-100)"
                    },
                    "sound_channel": {
                        "type": "str",
                        "value": "music",
                        "description": "
                                Current sound channel type, can be music, video, navigation, radio, conversation; the current environment has only one player, only one system can use the player at a time, so you need to modify the sound_channel field in the environment to use different systems.
                                - Please set to conversation when making/receiving calls or adjusting call volume
                                - Please set to music when playing music or adjusting music volume
                                - Please set to navigation when adjusting navigation volume, starting navigation, switching destinations, adding/removing waypoints, turning on/off announcements, or switching announcement modes
                                - Please set to radio when playing radio stations or adjusting radio volume
                                - Please set to video when adjusting video volume or playing videos
                                "
                    },
                    "unit_system": {
                        "type": "str",
                        "value": "mile",
                        "description": "Distance unit system, supports mile or kilometer"
                    }
                },
                "description": "World environment",
                "type": "type"
            }
}

Assistant:
The user needs to turn up the volume
```python
vw['environment']['value']['volume']['value'] = 60
```
Next, please generate state transition code to solve the user's request based on the current status of the system.
"""
    return instruction

def clean_status(messages):
    """
    Search for the first user message from the end backwards, and directly modify the original message list,
    delete "Current system status:" and its subsequent content in that message
    
    Args:
        messages (list): List containing message dictionaries
    """
    
    # Traverse messages from back to front
    for i in range(len(messages) - 1, -1, -1):
        message = messages[i]
        
        # Find user message
        if message["role"] == "user" and "Current system status:" in message["content"]:
            content = message["content"]
            status_index = content.find("Current system status:")
            
            if status_index != -1:
                # Keep only content before "Current system status:"
                messages[i]["content"] = content[:status_index].strip()

def get_modules(query, world_dict, agent_client):
    instruction = """
    You are a vehicle AI assistant. Given the current state of in-vehicle devices and a user query related to these devices, you need to identify and select the relevant device modules that should handle the query.

    ## Task Requirements:
    - Analyze the user query and current system status
    - Select the most relevant device modules (maximum 6 modules per query)
    - Return the selected modules in the specified format

    ## Output Format:
    <modules>
    module1
    module2
    module3
    </modules>

    ## Guidelines:
    1. Each module name should match exactly with the keys in the system status dictionary
    2. Separate multiple modules with newlines
    3. Only select modules that are directly relevant to fulfilling the user's request
    4. Consider the current state and capabilities of each module
    5. Prioritize modules that are most likely to be needed for the task

    ## Example:

    User:
    Play the video I've downloaded
    Current System Status:
    {
        "video": {
            "value": {
                "current_video": {
                    "value": {
                        "video_id": {
                            "value": "dl_001",
                            "type": "str",
                            "description": "Unique identifier for video"
                        },
                        "title": {
                            "value": "Highway Safety Tutorial",
                            "type": "str",
                            "description": "Title of the video"
                        },
                        "description": {
                            "value": "Learn about best practices for highway driving and safety tips",
                            "type": "str",
                            "description": "Description of the video"
                        }
                    },
                    "type": "VideoItem",
                    "description": "Currently selected video"
                },
                "downloaded_videos": {
                    "value": [
                        {
                            "video_id": {
                                "value": "dl_001",
                                "type": "str",
                                "description": "Unique identifier for video"
                            },
                            "title": {
                                "value": "City Night Drive",
                                "type": "str",
                                "description": "Title of the video"
                            },
                            "description": {
                                "value": "Exploring the city streets at night with ambient lighting",
                                "type": "str",
                                "description": "Description of the video"
                            }
                        }
                    ],
                    "type": "List[VideoItem]",
                    "description": "List of downloaded videos"
                }
            },
            "description": "Video system for media playback",
            "type": "Video"
        },
        "radio": {
            "value": {
                "_history": {
                    "type": "List[RadioStation]",
                    "value": [
                        {
                            "name": {
                                "type": "str",
                                "value": "Indie Music Channel",
                                "description": "Name of the radio station"
                            },
                            "frequency_value": {
                                "type": "str",
                                "value": "90.5 MHz",
                                "description": "Frequency value of the radio station"
                            },
                            "city": {
                                "type": "str",
                                "value": "Portland",
                                "description": "City where the radio station is available"
                            },
                            "app_name": {
                                "type": "str",
                                "value": "Independent Music",
                                "description": "App name used to play this radio station"
                            },
                            "timestamp": {
                                "type": "float",
                                "value": "2025-04-13 11:00:00",
                                "description": "Timestamp when this station was last played"
                            }
                        }
                    ],
                    "description": "History of played radio stations (most recent first)"
                },
                "_collection": {
                    "type": "List[RadioStation]",
                    "value": [
                        {
                            "name": {
                                "type": "str",
                                "value": "Indie Music Channel",
                                "description": "Name of the radio station"
                            },
                            "frequency_value": {
                                "type": "str",
                                "value": "90.5 MHz",
                                "description": "Frequency value of the radio station"
                            },
                            "city": {
                                "type": "str",
                                "value": "Portland",
                                "description": "City where the radio station is available"
                            },
                            "app_name": {
                                "type": "str",
                                "value": "Independent Music",
                                "description": "App name used to play this radio station"
                            },
                            "timestamp": {
                                "type": "float",
                                "value": "2025-04-13 11:00:00",
                                "description": "Timestamp when this station was last played"
                            }
                        }
                    ],
                    "description": "Collection of favorite radio stations"
                }
            },
            "description": "Radio system for audio streaming",
            "type": "Radio"
        },
        "navigation": {
            "value": {
                "current_location": {
                    "value": {
                        "latitude": 45.5152,
                        "longitude": -122.6784,
                        "address": "Portland, OR"
                    },
                    "type": "Location",
                    "description": "Current vehicle location"
                },
                "destination": {
                    "value": null,
                    "type": "Location",
                    "description": "Current navigation destination"
                }
            },
            "description": "Navigation and GPS system",
            "type": "Navigation"
        }
    }

    Assistant:
    The user wants to play a downloaded video. The video module contains downloaded videos and current video information, making it the primary module needed to handle this request. The radio and navigation modules are not relevant for this specific task.
    <modules>
    video
    </modules>
    """

    prompt = f"""
{query}
Current System Status:
{world_dict}
"""
    messages = [{"role":"system","content": instruction}]
    messages.append({"role":"user","content": prompt})
    response, total_token_length, prompt_token_length, completion_token_length = agent_client.chat(messages)
    modules = extract_text(response, r'<modules>(.*?)</modules>').split('\n')
    modules.append("environment")
    print(f"<<<<<<<Query Analysis>>>>>>>\n{query}\n{modules}")
    
    return messages,response, prompt_token_length, completion_token_length, modules

def process_task(task, task_id, agent_client, reflect_num, sample, plan, module_num):
    """
    Process tasks in separate threads
    
    Args:
        task: Task to process
        task_id: Task ID
    
    Returns:
        Processing result or None (if error)
    """
    try:
        tqdm.write(f"Starting task {task_id}")
        # Create a new local environment
        local_vars = {
            'vw': VehicleWorld()
        }
        # Initialize the environment
        inits_str = task['inits'].replace("\\n","\n")
        print(execute(f"from module import *\n{inits_str}", local_vars=local_vars, global_vars=None))
        local_vars = {
            'vw': local_vars["vw"].to_dict()
        }
        turns_result = []
        input_token_list = []
        output_token_list = []
        r = []
        instruction = generate_state_instruction(sample)
        messages = [{"role": "system", "content": instruction}]
        # Iterate through queries for solving
        for idx, query in enumerate(task["querys"]):
            tqdm.write(f"Processing {idx} query:\n{query}")
            # Clear previous round's system status at the beginning of each round
            clean_status(messages)
            get_modules_messages, response, prompt_token_length, completion_token_length, modules = get_modules(query, local_vars["vw"], agent_client)
            if module_num > 0:
                add_modules(modules, module_num)
            input_token_list.append(prompt_token_length)
            output_token_list.append(completion_token_length)
            r.append({"query": query, "response": response})
            previous_world_dict = copy.deepcopy(local_vars["vw"])
            if plan:
                plan_instruction = generate_plan_instruction()
                plan_messages = [{"role":"system","content":plan_instruction}]
                plan_messages.append({"role": "user", "content":query})
                action_plan, total_token_length, prompt_token_length, completion_token_length = agent_client.chat(plan_messages)
                input_token_list.append(prompt_token_length)
                output_token_list.append(completion_token_length)
                messages.append({"role": "user", "content": f"{query}\nCurrent system status:\nvw = {get_current_world_dict(modules, local_vars['vw'])}\nThe analysis for the current query is as follows:\n{action_plan}"})
            else:
                messages.append({"role": "user", "content": f"{query}\nCurrent system status:\nvw = {get_current_world_dict(modules, local_vars['vw'])}"})
            
            # Call model to generate code
            tqdm.write(f"Predicting actions...")
            response, total_token_length, prompt_token_length, completion_token_length = agent_client.chat(messages)
            input_token_list.append(prompt_token_length)
            output_token_list.append(completion_token_length)
            messages.append({"role": "assistant", "content": response})
            
            # Execute code
            tqdm.write(f"Executing actions...")
            execute_code = extract_text(response, r'```python(.*?)```')
            execute_result = execute(execute_code, local_vars=local_vars)
            messages.append({"role": "user", "content": f"Code execution results:{execute_result}\nCurrent system status:\nvw = {get_current_world_dict(modules, local_vars['vw'])}"})
            for i in range(reflect_num):
                tqdm.write(f"Reflecting {i} turn...")
                # Call model to generate code
                tqdm.write(f"Predicting actions...")
                response,total_token_length,prompt_token_length,completion_token_length = agent_client.chat(messages)
                input_token_list.append(prompt_token_length)
                output_token_list.append(completion_token_length)
                messages.append({"role": "assistant", "content": response})
                
                # Execute code
                tqdm.write(f"Executing actions...")
                execute_code = extract_text(response, r'```python(.*?)```')
                execute_result = execute(execute_code, local_vars=local_vars)
                messages.append({"role": "user", "content": f"Code execution results:{execute_result}\nCurrent system status:\nvw = {get_current_world_dict(modules, local_vars['vw'])}"})
                identical = compare_objects_values(task["worlds"][idx], task["worlds"][idx + 1], get_current_world_dict(modules, previous_world_dict), get_current_world_dict(modules, local_vars['vw']))["identical"]

                # If the worlds are identical for two consecutive steps, it means the model has finished reflecting
                if identical:
                    break
            tqdm.write(f"End Reflecting.")
            
            # End of current query round
            turn_result = calculate_turn_result(task["worlds"][idx], task["worlds"][idx + 1], previous_world_dict, local_vars["vw"])
            previous_world_dict = copy.deepcopy(local_vars["vw"])
            # Summarize current round conversation
            messages[-1] = messages[-1] | turn_result
            turns_result.append(turn_result)
        
        # Calculate task-level average metrics
        task_result = {
            "raw": task["raw"],
            "r": r,
            "messages": messages,
            "f1_positive": statistics.mean([t["f1_positive"] for t in turns_result if "f1_positive" in t]),
            "f1_negative": statistics.mean([t["f1_negative"] for t in turns_result if "f1_negative" in t]),
            "change_accuracy": statistics.mean([t["change_accuracy"] for t in turns_result if "change_accuracy" in t]),
            "input_token":statistics.mean(input_token_list),
            "output_token": statistics.mean(output_token_list),
            "total_output":sum(output_token_list),
            "task_id": task_id
        }
        
        tqdm.write(f"Task {task_id} completed successfully")
        return task_result
            
    except Exception as e:
        # Record error information if error occurs
        stack_trace = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        print(f"Task {task_id} processing error:\n{stack_trace}")
        return None

def sfc_evaluation(tasks_path="../database/tasks", max_workers=4, sample_size=3000, api_base="", api_key="", model="", reflect_num=0, module_num=0, sample=True, plan=False, prefix=""):
    """
    Evaluate tasks using thread pool and display progress bar.
    If output directory already exists and has completed batches, continue executing unfinished batches.
    """
    random.seed(42)
    total_tasks = read_tasks(tasks_path, module_num=module_num)
    results = []
    if not sample_size:
        sample_size = len(total_tasks)
        
    # Determine if sampling is needed
    if sample_size >= len(total_tasks):
        sample_tasks = total_tasks  # Use all tasks directly, without shuffling order
        print(f"Requested sample size {sample_size} is greater than or equal to total available tasks {len(total_tasks)}, will use all tasks.")
    else:
        sample_tasks = random.sample(total_tasks, sample_size)
        print(f"Randomly sampling {sample_size} tasks from {len(total_tasks)} tasks for evaluation.")
    
    agent_client = AgentClient(api_base=api_base, api_key=api_key, model=model)
    print(f"Starting evaluation, {len(sample_tasks)} tasks in total, using {max_workers} threads...")

    # Create output directory
    output_dir = f"outputs/{prefix}_{sample_size}_reflect_num_{reflect_num}_module_num_{module_num}_sample_{sample}_plan_{plan}_{model.replace('/', '_')}_sfc_result"
    os.makedirs(output_dir, exist_ok=True)

    # Check completed batches
    completed_batches = []
    
    # Find all existing batch files
    existing_batch_files = glob.glob(os.path.join(output_dir, "error_batch_*.json"))
    if existing_batch_files:
        print(f"Found {len(existing_batch_files)} completed batch files, loading completed results...")
        
        # Load results from each batch file
        for batch_file in existing_batch_files:
            try:
                # Get batch number from filename
                batch_num = int(os.path.basename(batch_file).split("_")[-1].split(".")[0])
                completed_batches.append(batch_num)
                
                # Load results from completed batch
                with open(batch_file, 'r', encoding='utf-8') as f:
                    batch_results = json.load(f)
                    for res in batch_results:
                        results.append(res)
                
                print(f"Loaded {len(batch_results)} results from batch {batch_num}")
            except Exception as e:
                logging.exception(f"Error loading batch file {batch_file}: {str(e)}")
    
    batch_size=100
    # Initialize thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Process tasks in batches
        for i in range(0, len(sample_tasks), batch_size):
            batch_num = i // batch_size + 1
            
            # If this batch is already completed, skip processing
            if batch_num in completed_batches:
                print(f"Batch {batch_num} already completed, skipping processing")
                continue
                
            batch = sample_tasks[i:i + batch_size]  # Get current batch tasks
            batch_results = []  # Store current batch results
            
            futures = [
                executor.submit(
                    process_task,
                    task,
                    idx + i,  # Index offset
                    agent_client,
                    reflect_num,
                    sample,
                    plan,
                    module_num
                )
                for idx, task in enumerate(batch)
            ]
                
            # Use tqdm to display batch progress
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc=f"Processing batch {batch_num}",
                unit="task",
            ):
                try:
                    res = future.result(timeout=600)  # Catch timeout tasks
                    if res:
                        batch_results.append(res)
                        results.append(res)
                except Exception as e:
                    logging.exception(f"Task execution exception: {str(e)}")
            
            # Save current batch results after each batch completion
            batch_error_path = os.path.join(output_dir, f"error_batch_{batch_num}.json")
            save_json_file(batch_results, batch_error_path)
            print(f"Batch {batch_num} results saved to {batch_error_path}")

    # If no results, output prompt
    if not results:
        print("No valid results to calculate statistics.")
        return results

    # Calculate overall metrics average for all batches and output
    metric = {
        "f1_positive": statistics.mean(r.get("f1_positive", 0) for r in results),
        "f1_negative": statistics.mean(r.get("f1_negative", 0) for r in results),
        "change_accuracy": statistics.mean(r.get("change_accuracy", 0) for r in results),
        "completed_tasks": len(results),
        "input_tokens": statistics.mean(r.get("input_token", 0) for r in results),
        "output_tokens": statistics.mean(r.get("output_token", 0) for r in results),
        "total_tasks": len(sample_tasks)
    }

    # Save final metrics data
    metric_path = os.path.join(output_dir, "metric.json")
    save_json_file(metric, metric_path)
    print(f"Overall metrics data saved to {metric_path}")

    # Save all log results as error file
    error_path = os.path.join(output_dir, "error.json")
    save_json_file(results, error_path)
    print(f"Overall log results saved to {error_path}")

    return results, metric_path, error_path
    
if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Execute evaluation tasks")
    
    # Add arguments
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of worker threads")
    parser.add_argument("--sample_size", type=int, default=50, help="Sample size")
    parser.add_argument("--api_base", type=str, required=True, help="API base URL")
    parser.add_argument("--api_key", type=str, required=True, help="API key")
    parser.add_argument("--model", type=str, required=True, help="Model name")
    parser.add_argument("--reflect_num", type=int, default=0, help="Number of reflections")
    parser.add_argument("--module_num", type=int, default=0, help="Number of additional modules")
    parser.add_argument("--sample", action="store_true", help="Whether to enable samples, include --sample for True, otherwise False")
    parser.add_argument("--plan", action="store_true", help="Whether to enable planning, include --plan for True, otherwise False")
    parser.add_argument("--prefix", type=str, default="", help="File prefix")
    
    # Parse arguments
    args = parser.parse_args()
    
    sfc_evaluation(
        max_workers=args.max_workers,
        sample_size=args.sample_size,
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        reflect_num=args.reflect_num,
        module_num=args.module_num,
        sample=args.sample,
        plan=args.plan,
        prefix=args.prefix
    )