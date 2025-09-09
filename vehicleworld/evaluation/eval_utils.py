import json
import os
import random
import re
import sys
sys.path.append('../')
from utils import modules_dict

def extract_text(response, pattern):
    """
    Extract all content from response and organize by lines
    
    Args:
    response (str): Input text string
    
    Returns:
    str: Extracted API call content, each call on one line
    """
    api_calls = re.findall(pattern, response, re.DOTALL)
    
    api_calls = [call.strip() for call in api_calls]
    
    return '\n'.join(api_calls)

def add_modules(modules, module_num=0):
    random.seed(42)
    # Filter out existing keys and randomly select num modules
    available_modules = [key for key in modules_dict if key not in modules]
    
    select_modules = random.sample(available_modules, min(module_num, len(available_modules)))
    modules.extend(select_modules)

def read_tasks(tasks_path="", module_num=0):
    """
    Reads task data from the database.
    
    Args:
        database_path (str): Path to the tasks database directory
        task_path (str, optional): Specific task path to load (e.g., "navigation/20250414130915")
                                   If provided, only this task will be loaded
    
    Returns:
        list: List of task dictionaries with their data
    """
    tasks = []
    
    for task_dir in sorted(os.listdir(tasks_path)):
        task_dir_path = os.path.join(tasks_path, task_dir)
        if os.path.isdir(task_dir_path):
            for sub_task_dir in sorted(os.listdir(task_dir_path)):
                sub_task_path = os.path.join(task_dir_path, sub_task_dir)
                if os.path.isdir(sub_task_path):
                    querys_path = os.path.join(sub_task_path, "querys")
                    modules_path = os.path.join(sub_task_path, "modules")
                    inits_path = os.path.join(sub_task_path, "inits")
                    raw_path = os.path.join(sub_task_path, "raw")
                    worlds_path = os.path.join(sub_task_path, "worlds.json")
                    
                    # Read query file content
                    with open(querys_path, 'r', encoding='utf-8') as f:
                        querys = [querys.strip() for querys in f.read().split('\n') if querys.strip()]
                    
                    # Read modules file content
                    with open(modules_path, 'r', encoding='utf-8') as f:
                        modules = [modules.strip() for modules in f.read().split('\n') if modules.strip()]
                    # World complexity experiment
                    if module_num > 0:
                        add_modules(modules, module_num)
                    
                    # Read worlds.json file
                    with open(worlds_path, 'r', encoding='utf-8') as f:
                        worlds = json.load(f)
                    
                    # Read inits file content
                    with open(inits_path, 'r', encoding='utf-8') as f:
                        inits = f.read()

                    # Read raw file content
                    with open(raw_path, 'r', encoding='utf-8') as f:
                        raw = f.read()
                    
                    tasks.append({
                        "id": sub_task_dir,
                        "querys": querys,
                        "modules": modules,
                        "worlds": worlds,
                        "inits": inits,
                        "raw": raw
                    })

    return tasks

def collect_values(obj, paths_map, path=""):
    """Collect important values from object"""
    if isinstance(obj, dict):
        # Handle special value objects
        if "type" in obj and "value" in obj:
            if obj["type"] in ["int", "str", "bool", "float"]:
                # Record value object
                paths_map[path] = obj["value"]
            
            # Handle cases where value is a list
            if isinstance(obj["value"], list):
                for index, item in enumerate(obj["value"]):
                    # Iterate through list elements for collection
                    new_path = f"{path}[{index}]"
                    collect_values(item, paths_map, new_path)
                
            if isinstance(obj["value"], dict):
                # Recursively process all values in dictionary
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    collect_values(value, paths_map, new_path)
            
            return
        
        # Recursively process all values in dictionary
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            collect_values(value, paths_map, new_path)
    
    # Handle lists
    elif isinstance(obj, list):
        # Record list length
        paths_map[path] = len(obj)
        
        # Recursively process list elements
        for i, item in enumerate(obj):
            collect_values(item, paths_map, f"{path}[{i}]")
    # It's a basic data type
    else:
        paths_map[path] = obj

def calculate_turn_result(world1, world2, world3, world4):
    """
    Calculate object change metrics based on comparison of expected and actual changes
    
    Args:
        world1: Original/reference object
        world2: Expected final object
        world3: Predicted initial object
        world4: Predicted final object
    
    Returns:
        dict: Contains difference list, TP/FP counts, change accuracy and F1 score
    """
    # Initialize result
    result = {
        "differences": [],
        "TP": 0,              # Should change and actually changed
        "FP": 0,              # Should not change but actually changed
        "negative_TP": 0,     # Should not change and actually didn't change
        "negative_FP": 0,     # Should change but actually didn't change
        "correctly_changed": 0, # Number of correctly changed items
    }
    
    # Collect value mappings of objects
    paths1 = {}  # Original reference object
    paths2 = {}  # Expected final object
    paths3 = {}  # Predicted initial object
    paths4 = {}  # Predicted final object
    
    # Collect values
    collect_values(world1, paths1)
    collect_values(world2, paths2)
    collect_values(world3, paths3)
    collect_values(world4, paths4)
    
    def get_trend(val1, val2):
        """Determine numerical change trend"""
        if val1 < val2: return "increase"
        elif val1 > val2: return "decrease"
        else: return "same"
    
    # Step 1: Analyze world1 and world2 to determine which paths should change and which should not
    should_change_paths = []  # List of paths that should change
    should_not_change_paths = []  # List of paths that should not change
    
    # Get all paths in world1 and world2
    all_ref_paths = set(paths1.keys()) | set(paths2.keys())
    
    for path in all_ref_paths:
        has_path1 = path in paths1
        has_path2 = path in paths2
        
        # Case 1: Path exists in both world1 and world2
        if has_path1 and has_path2:
            val1 = paths1[path]
            val2 = paths2[path]
            
            # Check if it should change
            if val1 != val2:
                should_change_paths.append((path, val1, val2))
            else:
                should_not_change_paths.append(path)
        
        # Case 2: Path only exists in world1 - should be deleted
        elif has_path1 and not has_path2:
            should_change_paths.append((path, paths1[path], None))  # None means should be deleted
        
        # Case 3: Path only exists in world2 - should be added
        elif not has_path1 and has_path2:
            should_change_paths.append((path, None, paths2[path]))  # None means should be added
    
    # Step 2: Analyze world3 and world4 to check actual changes
    # For each path that should change, check if it actually changed
    for path_info in should_change_paths:
        path, expected_old, expected_new = path_info
        
        has_path3 = path in paths3
        has_path4 = path in paths4
        
        # Case 1: Should modify existing value
        if expected_old is not None and expected_new is not None:
            if has_path3 and has_path4:
                val3 = paths3[path]
                val4 = paths4[path]
                
                # Check if it actually changed
                if val3 != val4:
                    # Actually changed
                    result["TP"] += 1
                    
                    # Check if the change is correct
                    if isinstance(expected_old, (int, float)) and isinstance(val3, (int, float)):
                        # Use trend comparison for numerical types
                        expected_trend = get_trend(expected_old, expected_new)
                        actual_trend = get_trend(val3, val4)
                        
                        if expected_trend == actual_trend:
                            result["correctly_changed"] += 1
                        else:
                            result["differences"].append(f"{path}: Different trend (should be {expected_trend}, actual {actual_trend})")
                    elif expected_new == val4:
                        # Use exact comparison for other types
                        result["correctly_changed"] += 1
                    else:
                        result["differences"].append(f"{path}: Different value (should be {expected_new}, actual {val4})")
                else:
                    # Should change but didn't change
                    result["negative_FP"] += 1 
                    result["differences"].append(f"{path}: Should change but didn't change")
            elif not has_path3 and has_path4:
                # Added, but should modify
                result["negative_FP"] += 1 
                result["differences"].append(f"{path}: Should modify but was added")
            elif has_path3 and not has_path4:
                # Deleted, but should modify
                result["negative_FP"] += 1 
                result["differences"].append(f"{path}: Should modify but was deleted")
            else:
                # Doesn't exist on both sides, cannot modify
                result["negative_FP"] += 1 
                result["differences"].append(f"{path}: Doesn't exist, cannot modify")
        
        # Case 2: Should delete
        elif expected_old is not None and expected_new is None:
            if has_path3 and not has_path4:
                # Successfully deleted
                result["TP"] += 1
                result["correctly_changed"] += 1
            else:
                # Failed to delete
                result["negative_FP"] += 1 
                if has_path3 and has_path4:
                    result["differences"].append(f"{path}: Should delete but not deleted")
                elif not has_path3 and not has_path4:
                    result["differences"].append(f"{path}: Doesn't exist originally, no need to delete")
                else:
                    result["differences"].append(f"{path}: Should delete but was added")
        
        # Case 3: Should add
        elif expected_old is None and expected_new is not None:
            if not has_path3 and has_path4:
                # Successfully added
                result["TP"] += 1
                
                val4 = paths4[path]
                # Check if added value is correct
                if expected_new == val4:
                    result["correctly_changed"] += 1
                else:
                    result["differences"].append(f"{path}: Added value incorrect (should be {expected_new}, actual {val4})")
            else:
                # Failed to add
                result["negative_FP"] += 1 
                if has_path3 and has_path4:
                    result["differences"].append(f"{path}: Should add but already exists")
                elif has_path3 and not has_path4:
                    result["differences"].append(f"{path}: Should add but was deleted")
                else:
                    result["differences"].append(f"{path}: Should add but not added")
    
    # For each path that should not change, check if it actually changed
    for path in should_not_change_paths:
        has_path3 = path in paths3
        has_path4 = path in paths4
        
        if has_path3 and has_path4:
            val3 = paths3[path]
            val4 = paths4[path]
            
            if val3 == val4:
                # Correctly remained unchanged
                result["negative_TP"] += 1
            else:
                # Should not change but changed
                result["FP"] += 1 
                result["differences"].append(f"{path}: Should not change but changed ({val3} -> {val4})")
        elif has_path3 and not has_path4:
            # Should not change but was deleted
            result["FP"] += 1 
            result["differences"].append(f"{path}: Should not change but was deleted")
        elif not has_path3 and has_path4:
            # Should not change but was added (doesn't exist in world3 but exists in world4)
            result["FP"] += 1 
            result["differences"].append(f"{path}: Doesn't exist in world3 but was added in world4")
    
    # Check for unexpected additions in world4
    for path in paths4:
        if path not in all_ref_paths and path not in paths3:
            # Unexpected addition
            result["FP"] += 1 
            result["differences"].append(f"{path}: Unexpected addition")

    # Calculate change accuracy
    total_should_changed = len(should_change_paths)
    if total_should_changed > 0:
        result["change_accuracy"] = result["correctly_changed"] / total_should_changed
    else:
        result["change_accuracy"] = 1.0
    
    # Calculate F1 score - measure ability to change
    if total_should_changed > 0:
        # Precision: TP / (TP + FP)
        precision = result["TP"] / (result["TP"] + result["FP"]) if (result["TP"] + result["FP"]) > 0 else 0
        # Recall: TP / total_should_changed
        recall = result["TP"] / total_should_changed
        # F1 score
        result["f1_positive"] = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    else:
        # Precision: TP / (TP + FP)
        precision = result["TP"] / (result["TP"] + result["FP"]) if (result["TP"] + result["FP"]) > 0 else 1
        # Recall: TP / total_should_changed
        recall = 1
        # F1 score
        result["f1_positive"] = 2 * precision * recall / (precision + recall)
    
    # Calculate F1 score - measure ability to not change
    total_should_unchanged = len(should_not_change_paths)
    if total_should_unchanged > 0:
        # Precision: negative_TP / (negative_TP + negative_FP)
        precision = result["negative_TP"] / (result["negative_TP"] + result["negative_FP"]) if (result["negative_TP"] + result["negative_FP"]) > 0 else 0
        # Recall: negative_TP / total_should_unchanged
        recall = result["negative_TP"] / total_should_unchanged
        # F1 score
        result["f1_negative"] = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    else:
        # Precision: negative_TP / (negative_TP + negative_FP)
        precision = result["negative_TP"] / (result["negative_TP"] + result["negative_FP"]) if (result["negative_TP"] + result["negative_FP"]) > 0 else 1
        # Recall: negative_TP / total_should_changed
        recall = 1
        # F1 score
        result["f1_negative"] = 2 * precision * recall / (precision + recall)
    
    return result

def compare_objects_values(world1, world2, world3, world4):
    """
    Compare int, str and bool type value fields in four objects
    Stop comparing when first difference is found
    
    Args:
        world1: Original/reference object
        world2: Expected final object
        world3: Predicted initial object
        world4: Predicted final object
    
    Returns:
        dict: Contains whether objects are identical and the first difference found
    """
    result = {"identical": True, "difference": ""}
    
    # Collect value mappings of objects
    paths1 = {}  # Original reference object
    paths2 = {}  # Expected final object
    paths3 = {}  # Predicted initial object
    paths4 = {}  # Predicted final object
    
    # Collect values
    collect_values(world1, paths1)
    collect_values(world2, paths2)
    collect_values(world3, paths3)
    collect_values(world4, paths4)
    
    def get_trend(val1, val2):
        """Determine numerical change trend"""
        if val1 < val2: return "increase"
        elif val1 > val2: return "decrease"
        else: return "same"
    
    # Step 1: Analyze world1 and world2 to determine which paths should change and which should not
    should_change_paths = []  # List of paths that should change
    should_not_change_paths = []  # List of paths that should not change
    
    # Get all paths in world1 and world2
    all_ref_paths = set(paths1.keys()) | set(paths2.keys())
    
    for path in all_ref_paths:
        has_path1 = path in paths1
        has_path2 = path in paths2
        
        # Case 1: Path exists in both world1 and world2
        if has_path1 and has_path2:
            val1 = paths1[path]
            val2 = paths2[path]
            
            # Check if it should change
            if val1 != val2:
                should_change_paths.append((path, val1, val2))
            else:
                should_not_change_paths.append(path)
        
        # Case 2: Path only exists in world1 - should be deleted
        elif has_path1 and not has_path2:
            should_change_paths.append((path, paths1[path], None))  # None means should be deleted
        
        # Case 3: Path only exists in world2 - should be added
        elif not has_path1 and has_path2:
            should_change_paths.append((path, None, paths2[path]))  # None means should be added
    
    # Step 2: Analyze world3 and world4 to check actual changes
    
    # First check each path that should change
    for path_info in should_change_paths:
        # Early exit
        if not result["identical"]:
            break
            
        path, expected_old, expected_new = path_info
        has_path3 = path in paths3
        has_path4 = path in paths4
        
        # Case 1: Should modify existing value
        if expected_old is not None and expected_new is not None:
            if has_path3 and has_path4:
                val3 = paths3[path]
                val4 = paths4[path]
                
                # Check if it actually changed and changed correctly
                if val3 == val4 and val3 != expected_old:  # Didn't change but should have changed
                    result["identical"] = False
                    result["difference"] = f"{path}: Should change but didn't change"
                    break
                elif val3 != val4:  # Changed
                    if isinstance(expected_old, (int, float)) and isinstance(val3, (int, float)):
                        # Use trend comparison for numerical types
                        expected_trend = get_trend(expected_old, expected_new)
                        actual_trend = get_trend(val3, val4)
                        
                        if expected_trend != actual_trend:
                            result["identical"] = False
                            result["difference"] = f"{path}: Different trend (should be {expected_trend}, actual {actual_trend})"
                            break
                    elif val4 != expected_new:  # Use exact comparison for other types
                        result["identical"] = False
                        result["difference"] = f"{path}: Different value (should be {expected_new}, actual {val4})"
                        break
            else:  # Path doesn't exist
                result["identical"] = False
                if not has_path3 and has_path4:
                    result["difference"] = f"{path}: Should modify existing value but was added"
                elif has_path3 and not has_path4:
                    result["difference"] = f"{path}: Should modify existing value but was deleted"
                else:
                    result["difference"] = f"{path}: Should modify existing value but doesn't exist in predicted objects"
                break
        
        # Case 2: Should delete
        elif expected_old is not None and expected_new is None:
            if has_path4:  # Not deleted
                result["identical"] = False
                result["difference"] = f"{path}: Should delete but not deleted"
                break
        
        # Case 3: Should add
        elif expected_old is None and expected_new is not None:
            if not has_path4:  # Not added
                result["identical"] = False
                result["difference"] = f"{path}: Should add but not added"
                break
            else:  # Added, check if value is correct
                val4 = paths4[path]
                if val4 != expected_new:
                    result["identical"] = False
                    result["difference"] = f"{path}: Added value incorrect (should be {expected_new}, actual {val4})"
                    break
    
    # Check each path that should not change
    if result["identical"]:
        for path in should_not_change_paths:
            has_path3 = path in paths3
            has_path4 = path in paths4
            
            if has_path3 and has_path4:
                val3 = paths3[path]
                val4 = paths4[path]
                
                if val3 != val4:  # Should not change but changed
                    result["identical"] = False
                    result["difference"] = f"{path}: Should not change but changed ({val3} -> {val4})"
                    break
            elif not has_path4:  # Should not change but was deleted
                result["identical"] = False
                result["difference"] = f"{path}: Should not change but was deleted"
                break
    
    # Check if world4 has unexpected paths
    if result["identical"]:
        for path in paths4:
            if path not in all_ref_paths and path not in paths3:
                result["identical"] = False
                result["difference"] = f"{path}: Unexpected addition"
                break
    
    if not result["identical"]:
        print(f"Difference: {result['difference']}")
    
    return result

def get_current_world_dict(modules, world):
    """
    Get current world
    """
    temp_modules = set(modules) | {"environment"}  # Temporarily add one element
    current_world = {k: world[k] for k in world if k in temp_modules}
    return current_world