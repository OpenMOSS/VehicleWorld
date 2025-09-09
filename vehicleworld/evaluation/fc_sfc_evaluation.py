import json
import sys
from agent_client import AgentClient
from eval_utils import read_tasks, extract_text, calculate_turn_result, get_current_world_dict
sys.path.append('../')
from utils import save_json_file, execute, get_api_content
from vehicleworld import VehicleWorld
import statistics
import traceback
import logging
from tqdm import tqdm
import argparse
import random
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob

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

def generate_instruction(sample=True):
    """Create the instruction prompt with API content."""
    instruction =  f"""
You are an intelligent in-car AI assistant responsible for fulfilling user requests by calling the vehicle system API. Please ensure you understand user needs and complete tasks in the most efficient way.

**API Call Requirements**  
- Each code block can contain multiple related API calls, but should remain concise.
- Ensure the code can be executed directly, without non-code content other than comments.
- Code sections should be surrounded by ```python```.
- Only generate API calls, do not generate any additional code.

**System Feedback Handling**  
- The system will return execution results after each API call, including return values (success or failure) and any error messages.
- Carefully analyze each feedback to decide the next step. If an API call fails, analyze the reason and make corrections.

**Task Completion Standards**  
1. Choose the most efficient API combination to complete tasks, avoiding unnecessary code.
2. Correctly handle API errors and exception situations.
3. If the system status does not support the user's request, clearly decline.
"""
    if sample:
        instruction += """
**Example Task Flow**
User:
Navigate to the nearest gas station and turn up the navigation volume a bit
The user wants to go to a nearby gas station and turns up the navigation volume. the relevant device module to handle this query is the navigation.
<moduels>
navigation
</modules>
The following are the APIs associated with the device module:
--- NAVIGATION METHODS ---
Method name: vw.navigation.navigation_route_plan
API description:
def navigation_route_plan(self, address, placeOfDeparture="Current location"):
    '''
    Route planning, specify destination to start navigation.
    
    Args:
    address (str): Destination name/address.
    placeOfDeparture(str): Departure name/address
    Returns:
    dict: Result of the operation with route details.
    '''

Method name: vw.navigation.navigation_soundVolume_increase
API description:
def navigation_soundVolume_increase(self, value=None, degree=None):
    '''
    Increase navigation volume.
    
    Args:
    value (int, optional): Specific numeric amount to increase volume.
    degree (str, optional): Categorical level of increase.
    Valid values are "large", "little", "tiny",mutually exclusive with value.
    
    Returns:
    dict: Result of the operation with updated volume.
    '''
...

Assistant:
After understanding the available APIs, I'll plan a route to the nearest gas station for you:

```python
vw.navigation.navigation_route_plan("nearest gas station")
```

User:
Code execution results:
{{
  "success": True,
  "route": {{
    "destination": "nearest gas station",
    "distance": "3 km", 
    "duration": "10 minutes"
  }}
}}

Assistant:
Navigation has been successfully set to the nearest gas station, now I'll increase the navigation volume:

```python
vw.navigation.navigation_soundVolume_increase(degree="little")
```

User:
Code execution results:
{{
  "success": True,
  "old_volume": 30,
  "new_volume": 40,
  "sound_channel": "navigation"
}}

Assistant:
I have successfully completed the following operations for you:

Set navigation to the nearest gas station, approximately 3 kilometers away, with an estimated travel time of 10 minutes
Increased the navigation volume from 30 to 40, making it easier for you to hear the navigation instructions clearly
The navigation system is now active, and you can follow the guidance to the gas station. If you need any other assistance, please let me know.
"""
    return instruction

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
    print(f"<<<<<<<Query Analysis>>>>>>>\n{query}\n{modules}")
    
    return messages,response, prompt_token_length, completion_token_length, modules

def process_task(task, task_id, agent_client, reflect_num, sample, plan):
    try:
        # Create a new local environment
        local_vars = {
            'vw': VehicleWorld()
        }
        # Initialize the environment
        inits_str = task['inits'].replace("\\n","\n")
        print(execute(f"from module import *\n{inits_str}", local_vars=local_vars, global_vars=None))
        current_world_dict = get_current_world_dict(task["modules"], local_vars["vw"].to_dict())
        previous_world_dict = current_world_dict
        instruction = generate_instruction(sample)
        messages = [{"role": "system", "content": instruction}]
        turns_result = []
        input_token_list = []
        output_token_list = []
        r = []

        # Iterate through queries for solving
        for idx, query in enumerate(task["querys"]):
            tqdm.write(f"Processing {idx} query:\n{query}")
            get_modules_messages, response, prompt_token_length, completion_token_length, modules = get_modules(query, local_vars["vw"].to_dict(), agent_client)
            input_token_list.append(prompt_token_length)
            output_token_list.append(completion_token_length)
            r.append({"query": query, "response": response})
            query_analysis = f"{query}\n{response}\nThe following are the APIs associated with the device module:\n{get_api_content(modules)}"
            if plan:
                plan_instruction = generate_plan_instruction()
                plan_messages = [{"role":"system","content":plan_instruction}]
                plan_messages.append({"role": "user", "content":query})
                action_plan,total_token_length,prompt_token_length,completion_token_length = agent_client.chat(plan_messages)
                input_token_list.append(prompt_token_length)
                output_token_list.append(completion_token_length)
                messages.append({"role": "user", "content": f"{query}\nThe analysis for the current query is as follows:\n{action_plan}"})
            else:
                messages.append({"role": "user", "content": query_analysis})
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

            # Start reflection
            for i in range(reflect_num):
                tqdm.write(f"Reflecting {i} turn...")
                messages.append({"role": "user", "content": f"Code execution results:\n{execute_result}"})
                previous_execute_result = execute_result

                # Call model to generate code
                tqdm.write(f"Predicting actions...")
                response, total_token_length, prompt_token_length, completion_token_length = agent_client.chat(messages)
                input_token_list.append(prompt_token_length)
                output_token_list.append(completion_token_length)
                messages.append({"role": "assistant", "content": response})
                
                # Execute code
                tqdm.write(f"Executing actions...")
                execute_code = extract_text(response, r'```python(.*?)```')
                # If no code is generated in the current step, exit the reflection
                if count_non_comment_lines(execute_code) == 0:
                    break

                execute_result = execute(execute_code, local_vars=local_vars)
                # If the code returns the same result, exit the reflection
                if previous_execute_result == execute_result:
                    break 

            tqdm.write(f"End Reflecting.")
            
            # End of current query
            current_world_dict = get_current_world_dict(task["modules"], local_vars["vw"].to_dict())
            turn_result = calculate_turn_result(task["worlds"][idx], task["worlds"][idx + 1], previous_world_dict, current_world_dict)
            previous_world_dict = current_world_dict
            # Summarize current turn conversation
            messages[-1] = messages[-1] | turn_result
            turns_result.append(turn_result)
        
        # Calculate task-level average metrics
        task_result = {
            "raw": task["raw"],
            "r": r,
            "messages": messages,
            "f1_positive": statistics.mean([t["f1_positive"] for t in turns_result]),
            "f1_negative": statistics.mean([t["f1_negative"] for t in turns_result]),
            "change_accuracy": statistics.mean([t["change_accuracy"] for t in turns_result]),
            "input_token":statistics.mean(input_token_list),
            "output_token":statistics.mean(output_token_list),
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

def count_non_comment_lines(code_str: str) -> int:
    """
    Count the number of non-comment lines (excluding pure comment lines and empty lines) in code_str.
    Only recognizes line comments starting with '#', does not handle multi-line string comments.
    """
    count = 0
    for line in code_str.splitlines():
        s = line.strip()
        # Skip empty lines
        if not s:
            continue
        # Skip comment lines starting with '#'
        if s.startswith('#'):
            continue
        # Otherwise count as valid code line
        count += 1
    return count

def fc_sfc_evaluation(tasks_path="../database/tasks", max_workers=4, sample_size=3000, api_base="", api_key="", model="", reflect_num=3, sample=True, plan=False, prefix=""):
    """
    Evaluate tasks using thread pool and show progress bar.
    If output directory already exists and has completed batches, continue executing unfinished batches.
    """
    random.seed(42)
    total_tasks = read_tasks(tasks_path)
    results = []
    if not sample_size:
        sample_size = len(total_tasks)
        
    # Determine if sampling is needed
    if sample_size >= len(total_tasks):
        sample_tasks = total_tasks  # Use all tasks directly, don't shuffle order
        print(f"Requested sample size {sample_size} is greater than or equal to total available tasks {len(total_tasks)}, will use all tasks.")
    else:
        sample_tasks = random.sample(total_tasks, sample_size)
        print(f"Randomly selected {sample_size} tasks from {len(total_tasks)} total tasks for evaluation.")
    
    agent_client = AgentClient(api_base=api_base, api_key=api_key, model=model)
    print(f"Starting evaluation with {len(sample_tasks)} tasks, using {max_workers} threads...")

    # Create output directory
    output_dir = f"outputs/{prefix}_{sample_size}_reflect_num_{reflect_num}_sample_{sample}_plan_{plan}_{model.replace('/', '_')}_fc_sfc_result"
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
                    plan
                )
                for idx, task in enumerate(batch)
            ]
                
            # Use tqdm to show batch progress
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
            
            # Save current batch results after each batch completes
            batch_error_path = os.path.join(output_dir, f"error_batch_{batch_num}.json")
            save_json_file(batch_results, batch_error_path)
            print(f"Batch {batch_num} results saved to {batch_error_path}")

    # If no results, output prompt
    if not results:
        print("No valid results available for calculating statistics.")
        return results

    # Calculate metric averages and output
    metric = {
        "f1_positive": statistics.mean(r.get("f1_positive", 0) for r in results),
        "f1_negative": statistics.mean(r.get("f1_negative", 0) for r in results),
        "change_accuracy": statistics.mean(r.get("change_accuracy", 0) for r in results),
        "completed_tasks": len(results),
        "input_tokens": statistics.mean(r.get("input_token", 0) for r in results),
        "output_tokens": statistics.mean(r.get("output_token", 0) for r in results),
        "total_tasks": len(sample_tasks)
    }

    # Save metrics data
    metric_path = os.path.join(output_dir, "metric.json")
    save_json_file(metric, metric_path)
    print(f"Metrics data saved to {metric_path}")

    # Save log results as error file
    error_path = os.path.join(output_dir, "error.json")
    save_json_file(results, error_path)
    print(f"Log results saved to {error_path}")

    return results, metric_path, error_path

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Execute evaluation tasks")
    
    # Add parameters
    parser.add_argument("--max_workers", type=int, default=4, help="Maximum number of worker threads")
    parser.add_argument("--sample_size", type=int, default=50, help="Sample size")
    parser.add_argument("--api_base", type=str, required=True, help="API base URL")
    parser.add_argument("--api_key", type=str, required=True, help="API key")
    parser.add_argument("--model", type=str, required=True, help="Model name")
    parser.add_argument("--reflect_num", type=int, default=0, help="Number of reflections")
    parser.add_argument("--sample", action="store_true", help="Whether to enable examples, include --sample for True, otherwise False")
    parser.add_argument("--plan", action="store_true", help="Whether to enable examples, include --plan for True, otherwise False")
    parser.add_argument("--prefix", type=str, default="", help="File prefix")
    
    # Parse parameters
    args = parser.parse_args()
    
    fc_sfc_evaluation(
        max_workers=args.max_workers,
        sample_size=args.sample_size,
        api_base=args.api_base,
        api_key=args.api_key,
        model=args.model,
        reflect_num=args.reflect_num,
        sample=args.sample,
        plan=args.plan,
        prefix=args.prefix
    )