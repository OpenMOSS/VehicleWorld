import hashlib
import re
import os
import subprocess
import sys
sys.path.append('../')
from utils import delete_all_contents, modules_dict, capitalize_first
import tempfile
import shutil
from tqdm import tqdm 

def extract_scenarios(text):
    # Use regular expression to extract all <scenario> ... </scenario> paragraphs
    scenario_pattern = r"<scenario>(.*?)</scenario>"
    scenarios = re.findall(scenario_pattern, text, re.DOTALL)
    
    all_scenarios = []
    for scenario in scenarios:
        # Extract content from <inits> ... </inits>
        init_pattern = r"<inits>(.*?)</inits>"
        inits = re.search(init_pattern, scenario, re.DOTALL).group(1).strip()

        # Extract modules
        modules = []
        for module in modules_dict:
            if module in inits or capitalize_first(module) in inits:
                modules.append(module)

        # Extract content from <query> ... </query>
        query_pattern = r"<query>(.*?)</query>"
        queries = re.findall(query_pattern, scenario, re.DOTALL)
        
        # Extract content from <api_call> ... </api_call>
        api_call_pattern = r"<api_call>(.*?)</api_call>"
        api_calls = re.findall(api_call_pattern, scenario, re.DOTALL)
        
        all_scenarios.append({
            'queries': queries,
            'api_calls': api_calls,
            'inits': inits,
            'modules': modules,
            "raw": f"<scenario>{scenario}</scenario>"
        })
    return all_scenarios

def generate_unique_id(raw_text):
    """
    Generate unique folder name using scenario['raw']
    Use hash algorithm to ensure uniqueness
    """
    # Use MD5 hash to generate unique identifier
    hash_object = hashlib.md5(raw_text.encode('utf-8'))
    return hash_object.hexdigest()

def save_and_execute_files(scenarios, output_directory="tasks"):
    """
    Based on scenarios list, create timestamp folder for each scenario,
    and generate corresponding files under specified output_directory.
    Also write module list to module file.
    Only save files when execution is successful.
    Added progress bar display functionality.
    """

    success_count = 0
    failure_count = 0
    skipped_count = 0
    # Directly wrap scenarios iteration with tqdm
    for i, scenario in enumerate(tqdm(scenarios, desc="Processing scenarios", total=len(scenarios), 
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")):

        # Generate unique ID using scenario['raw']
      
        unique_id = generate_unique_id(scenario['raw'])
      
        # Check if folder already exists
        final_dir = os.path.join(output_directory, unique_id)
        if os.path.exists(final_dir):
            tqdm.write(f"⏭️ Scenario {i+1}: Skipped - Folder already exists ({unique_id})")
            skipped_count += 1
            continue
        # Create temporary directory
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as temp_dir:
            # Create all files in temporary directory
            # File 1: Save original text
            with open(os.path.join(temp_dir, "raw"), "w", encoding="utf-8") as f:
                f.write(f"{scenario['raw']}\n")
                    
            # File 2: Save queries to query file
            with open(os.path.join(temp_dir, "querys"), "w", encoding="utf-8") as f:
                for query in scenario['queries']:
                    f.write(f"{query}\n")
            
            # File 3: Save modules to modules file
            with open(os.path.join(temp_dir, "modules"), "w", encoding="utf-8") as f:
                for module in scenario['modules']:
                    f.write(f"{module}\n")
                    
            # File 4: Save inits to inits file
            with open(os.path.join(temp_dir, "inits"), "w", encoding="utf-8") as f:
                f.write(f"{scenario['inits']}")
                
            # File 5: Create Python execution file, including header, API calls and footer
            inits_str =scenario['inits'].replace("\\n", "\n")
            execute_code_str = f"""
import os
import sys
def find_root_dir():
    current_dir = os.path.abspath(os.getcwd())
    while True:
        if os.path.exists(os.path.join(current_dir, 'setup.py')) or os.path.exists(os.path.join(current_dir, 'README.md')):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # Reached filesystem root directory
            raise FileNotFoundError('Cannot find project root directory')
        current_dir = parent_dir
sys.path.append(f'{{find_root_dir()}}/vehicleworld')
from utils import save_json_file
from vehicleworld import *
from module import *
modules = {scenario['modules']}
modules.append('environment')
vw = VehicleWorld()
# Initialize world
{inits_str}
temp_world = vw.to_dict()
worlds = [{{k: temp_world[k] for k in temp_world if k in modules}}]
"""
            for api_call in scenario['api_calls']:
                temp_api_call = api_call.replace("\\n", "\n")
                execute_code_str += f"""
{temp_api_call}
temp_world = vw.to_dict()
worlds.append({{k: temp_world[k] for k in temp_world if k in modules}})
"""
            # File 6: World state list
            execute_code_str += "save_json_file(worlds, 'worlds.json')"
            with open(os.path.join(temp_dir, "execute.py"), "w", encoding="utf-8") as f:
                f.write(execute_code_str)
                
            # Execute generated Python file
            try:
                # Don't print detailed logs in progress bar, but store status
                current_dir = os.getcwd()
                os.chdir(temp_dir)
                
                process = subprocess.Popen([sys.executable, "execute.py"], 
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          text=True)
                stdout, stderr = process.communicate()
                
                if process.returncode == 0:
                    # Use tqdm.write to output success message without interfering with progress bar
                    tqdm.write(f"✅ Scenario {i+1}: Success")
                    success_count += 1
                    
                    # Execution successful, move files to final directory
                    final_dir = os.path.join(f"../{output_directory}", unique_id)
                    os.makedirs(final_dir, exist_ok=True)
                    
                    # Copy all files to final directory
                    for filename in os.listdir(temp_dir):
                        source = os.path.join(temp_dir, filename)
                        destination = os.path.join(final_dir, filename)
                        if os.path.isfile(source):
                            shutil.copy2(source, destination)
                else:
                    # Use tqdm.write to output failure message without interfering with progress bar
                    tqdm.write(f"❌ Scenario {i+1}: Failed - {stderr}")
                    failure_count += 1
                
                os.chdir(current_dir)
            except Exception as e:
                # Use tqdm.write to output exception message without interfering with progress bar
                tqdm.write(f"⚠️ Scenario {i+1}: Exception - {str(e)}")
                failure_count += 1
                os.chdir(current_dir)
    
    # Print final statistics
    print(f"\nExecution completed: {success_count} scenarios succeeded, {failure_count} scenarios failed.")
    print(f"Success rate: {success_count/len(scenarios)*100:.1f}%")
    
    return success_count, len(scenarios)

def main_entry(primary_dir, output_base="tasks"):
    """
    header_file: File name containing header code
    footer_file: File name containing footer code
    primary_dir: Primary directory containing several secondary directories, each containing files to be processed
    output_base: Root directory for generated output folders (default data)
    
    Module list is obtained by analyzing file names, assuming file name format like "10_module1&module2",
    take the part after "10_" and split by "&" to get module list.
    """
    # Delete all tasks
    delete_all_contents(output_base)
    for filename in os.listdir(primary_dir):
        if '.' not in filename: # Only process files without extension
            print(f"Processing subdirectory: {filename}")
            # Create a directory with the same name in output directory for this secondary directory
            output_dir = os.path.join(output_base, filename)
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(primary_dir, filename)
            if os.path.isfile(file_path):
                # Read current file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    scenarios_str = f.read()
                # Extract scenarios
                scenarios = extract_scenarios(scenarios_str)
                # Save files and execute scripts, save output in output_dir corresponding to current secondary directory
                save_and_execute_files(scenarios, output_directory=output_dir)

if __name__ == "__main__":
    main_entry("querys", output_base="tasks")