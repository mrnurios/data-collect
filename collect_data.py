import json
import os

# Data dictionary for cubes and their probabilities
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Load JSON data into a Python dictionary
    return data

def save_data(file_path, data):
    """
    Save data to a JSON file atomically to prevent corruption.
    """
    # Ensure backup directory exists
    backup_dir = "backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    temp_file = file_path + ".tmp"   
    backup_file_path = os.path.join(backup_dir, file_path + ".bak")

    try:
         # Create a backup of the original file (if it exists)
        if os.path.exists(file_path):
            os.replace(file_path, backup_file_path)  # Move current file to backup
        else:
            # If original file doesn't exist, just create an empty backup file
            with open(backup_file_path, 'w') as backup_file:
                json.dump({}, backup_file, indent=4)
    
        # Write to a temporary file first
        with open(temp_file, 'w') as file:
            json.dump(data, file, indent=4)

        # Move the temporary file to replace the original
        os.replace(temp_file, file_path)
        
        print(f"Data saved successfully to {file_path}.")
    except Exception as e:
        print(f"Error during saving: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)  # Clean up temporary file

def record_history(positions, results, history_file):
    """
    Record user inputs (positions and results) into a history file for undo purposes.
    """
    history = load_data(history_file)
    history_entry = {"positions": positions, "results": results}

    # Append the new entry
    history.setdefault("entries", []).append(history_entry)

    # Save updated history
    save_data(history_file, history)
    print("Action recorded for undo purposes.")

def undo_last_action(data, history_file, file_path):
    """
    Undo the last recorded action by reversing the changes in the data file.
    """
    history = load_data(history_file)
    if "entries" not in history or not history["entries"]:
        print("\nNo actions to undo.")
        return

    # Retrieve and remove the last entry
    last_entry = history["entries"].pop()
    positions = last_entry["positions"]
    results = last_entry["results"]

    # Reverse the changes in data
    for index, cube in enumerate(positions):
        pos = ['L', 'M', 'R'][index]  # Determine position
        try:
            data[cube][pos][results[index]] -= 1
        except KeyError:
            print(f"Undo failed: {cube}, {results[index]} not found. Skipping...")

    # Save the updated data and history
    save_data(file_path, data)
    save_data(history_file, history)
    print("\nLast action undone.")

def feed(data, r, p):
    positions = ['L', 'M', 'R']  # Mapping of indexes to position names
    for index, x in enumerate(p):  # x is cube position (e.g. WB, BG)
        pos = positions[index]  # Get position dynamically from the list
        data[x][pos][r[index]] += 1

def error_handle1(pos, data):
    while True:
        cube = input(f'{pos} Cube: ')
        if cube.upper() not in data:
            print('\nCube not in data. Try again.')
            continue
        else:
            return cube.upper()

def error_handle2(pos, data):
    while True:
        result = input(f"Result for {pos} Cube: ")
        if result.upper() not in data['WP']['L']:
            print('\nColor not in data. Try again.')
            continue
        else:
            return result.upper()

def main():
    spacer = '\n--------------------------------------------------------------------'
    while True:
        file_path = "data copy.json"
        history_file = "changes_" + file_path

        if not os.path.exists(history_file):
            template = {"entries": []}
            with open(history_file, 'w') as file:
                json.dump(template, file, indent=4)

        data = load_data(file_path)

        while True:
            print(spacer)
            print('\nFile:',file_path)
            prompt = input('\nIs the file correct? 1-Yes | 0-No (Select Number):')
            if prompt == "0":
                print('No')
                file_path = input('\nInput File Name/Path: ')
                continue
            elif prompt == "1":
                print('Yes')
                break
            else:
                print("Invalid input.")

        print(spacer)
        print()
        c_left = error_handle1('Left', data)
        c_middle = error_handle1('Middle', data)
        c_right = error_handle1('Right', data)

        positions = [c_left, c_middle, c_right]

        print()
        r_left = error_handle2('Left', data)
        r_middle = error_handle2('Middle', data)
        r_right = error_handle2('Right', data)

        results = [r_left, r_middle, r_right]

        while True:
            print(spacer)
            print(f'\n{c_left} (L): {r_left}\n{c_middle} (M): {r_middle}\n{c_right} (R): {r_right}')
            prompt=input('\n1-Save Data | 0-Cancel (Select Number):')
            if prompt=='0':
                print('Cancel')
                print('\nCancelling...')
                break
            elif prompt=='1':
                print('Save Data')
                feed(data, results, positions)
                save_data(file_path, data)
                record_history(positions, results, history_file)
                print('\nData Saved!')
                break
            else:
                print("Invalid input.")

        while True:
            print(spacer)
            print('\nUndo (U) | Next (Enter) | Exit (ESC):')
            prompt=input('\n1-Next | 2-Undo | 0-Exit (Select Number):')
            if prompt=='0':
                print('Exit')
                print("\nExiting program...")
                return
            elif prompt=='2':
                print('Undo')
                undo_last_action(data, history_file, file_path)
            elif prompt=='1':
                print('Next')
                break
            else:
                print("Invalid input.")

if __name__ == "__main__":
    main()
