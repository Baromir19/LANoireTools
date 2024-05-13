import os
import re

def sanitize_filename(filename): # additional function / useless for now
    filename = filename.replace('\\x04', '_')
    return re.sub(r'[^\w\-_\. ]', '_', filename)

def rename_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            if '.' not in filename:
                with open(file_path, 'rb') as file:
                    header = file.read(4)
                
                # HEADER READERS
                if header == b'FSB4':
                    with open(file_path, 'rb') as file:
                        file.seek(0x32)
                        new_filename = file.read(0x50 - 0x32).decode().strip('\x00')
                    new_filename = sanitize_filename(new_filename)
                    new_extension = '.fsb'
                elif header == b'ATB\x04':
                    new_filename = sanitize_filename(filename)
                    new_extension = '.atb'
                else:
                    # just for another ways
                    try:
                        new_extension = '.' + header.decode('ascii', 'ignore')
                    except UnicodeDecodeError:
                        new_extension = f'.{header.hex()}'
                    new_filename = sanitize_filename(filename)

                new_extension = sanitize_filename(new_extension)
                
                new_file_path = os.path.join(folder_path, new_filename + new_extension)

                # print(f'{new_file_path}')                
                # additional suffix for existed names
                suffix = 1
                while os.path.exists(new_file_path):
                    new_file_path = os.path.join(folder_path, f"{new_filename}_{suffix}{new_extension}")
                    suffix += 1
                
                os.rename(file_path, new_file_path)
                print(f"File renamed: {filename} -> {os.path.basename(new_file_path)}")

if __name__ == "__main__":
    folder_path = input("Enter the path for the folder with files: ")
    rename_files(folder_path)
