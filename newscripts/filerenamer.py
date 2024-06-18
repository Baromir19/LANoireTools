import os
import sys
from typing import Dict, Optional
from dictionaries import FILE_FULLNAME_DICTIONARY

class FileRenamer:
    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def get_new_filename(self, filename: str) -> Optional[str]:
        hex_string = None
        
        if filename.startswith("0x") and filename[2:10].isalnum():
            hex_string = filename[2:10]
        elif filename[:8].isdigit():
            hex_string = filename[:8]

        if hex_string is not None:
            try:
                hex_value = int(hex_string, 16)
                new_filename = FILE_FULLNAME_DICTIONARY.get(hex_value)
                if new_filename:
                    return new_filename
            except ValueError:
                pass

        return None

    def rename_files(self) -> None:
        if not os.path.exists(self.folder_path):
            print(f"Folder {self.folder_path} does not exist")
            return

        for filename in os.listdir(self.folder_path):
            if filename.endswith(".xml"):
                continue

            new_filename = self.get_new_filename(filename)
            if new_filename:
                new_dir = os.path.dirname(new_filename)
                if not os.path.exists(new_dir):
                    try:
                        os.makedirs(new_dir)
                    except OSError as e:
                        print(f"Error creating directory {new_dir}: {e}")
                        continue

                old_path = os.path.join(self.folder_path, filename)
                new_path = os.path.join(os.path.dirname(new_filename), os.path.basename(new_filename))
                try:
                    os.rename(old_path, new_path)
                    print(f"File {filename} moved to {new_path}")
                except FileExistsError as ex:
                    print(f"Impossible to move {filename} to {new_path}\n{ex}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("Enter folder path: ")

    renamer = FileRenamer(folder_path)
    renamer.rename_files()

    print("\nReady!")