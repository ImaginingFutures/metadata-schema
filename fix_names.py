import os
import re

def fix_names(path):
    """Ensures that the file and directory names do not contain spaces or parentheses."""

    for root, dirs, files in os.walk(path):
        for name in dirs:
            if name.startswith('.'):
                continue
            new_name = re.sub(r'[\s()]+', '_', name)  # Replace spaces and parentheses with underscores
            new_name = re.sub(r'[()]+', '', new_name) # Remove parentheses
            if new_name != name:
                #os.rename(os.path.join(root, name), os.path.join(root, new_name))
                print('Renamed directory: ' + name + ' to ' + new_name)
        for name in files:
            new_name = re.sub(r'[\s]+', '_', name)  # Replace spaces with underscores
            new_name = re.sub(r'[()]+', '', new_name) # Remove parentheses
            if new_name != name:
                os.rename(os.path.join(root, name), os.path.join(root, new_name))
                print('Renamed file: ' + name + ' to ' + new_name)

fix_names(os.getcwd())