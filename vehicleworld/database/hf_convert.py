import os
import csv
import sys

def csv_to_directory(csv_file, target_dir):
    """
    Reads a CSV file and creates a directory structure based on its content.

    Args:
        csv_file (str): The path to the input CSV file.
        target_dir (str): The path to the target directory where the structure will be created.
    """
    if not os.path.isfile(csv_file):
        # Using sys.stderr for error messages is a good practice.
        sys.stderr.write(f"Error: CSV file '{csv_file}' not found.\n")
        return

    os.makedirs(target_dir, exist_ok=True)

    # Handle large fields in CSV
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int / 10)

    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if not reader.fieldnames:
                sys.stderr.write("Error: CSV file is empty or has no header row.\n")
                return
                
            filenames = [header for header in reader.fieldnames if header != 'id']
            
            for row in reader:
                subdir_name = row.get('id')
                if not subdir_name:
                    # It's better to inform about skipped rows.
                    sys.stderr.write("Warning: Skipping a row because 'id' value is missing.\n")
                    continue
                
                full_subdir_path = os.path.join(target_dir, subdir_name)
                os.makedirs(full_subdir_path, exist_ok=True)

                for filename in filenames:
                    file_path = os.path.join(full_subdir_path, filename)
                    content = row.get(filename, "")
                    
                    try:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                    except IOError as e:
                        sys.stderr.write(f"Error: Could not write to file '{file_path}': {e}\n")
                        
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred while processing the CSV file: {e}\n")

if __name__ == "__main__":

    csv_to_directory("./VehicleWorld/VehicleWorld.csv", "tasks/scenarios")