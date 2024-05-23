import os, sys

from dictionaries import FILE_EXTENSIONS_DICTIONARY 

class FileRenamer:
    def __init__(self, folder_path, with_extension = True):
        self.folder_path = folder_path
        self.with_extension = with_extension # True = add extension / False = remove extension

    def rename_files(self):
        with open(self.folder_path + '\\renamed.txt', 'wt') as renamed_file:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    new_filename = ''
                    if self.with_extension:
                        self.process_file(file_path)
                    else:
                        self.remove_extension_if_magic(file_path)
                    if new_filename:
                        renamed_file.write(f"{filename} -> {new_filename}\n")

    def process_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                magic_bytes = file.read(4)
            if magic_bytes in FILE_EXTENSIONS_DICTIONARY:
                extension = '.' + FILE_EXTENSIONS_DICTIONARY[magic_bytes]
                new_filename = self.remove_extension(file_path) + extension
                os.rename(file_path, new_filename) # here exception
                return os.path.basename(new_filename)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return None

    def remove_extension_if_magic(self, file_path):
        with open(file_path, 'rb') as file:
            magic_bytes = file.read(4)
        if magic_bytes in FILE_EXTENSIONS_DICTIONARY:
            base_name = self.remove_extension(file_path)
            os.rename(file_path, base_name)
            return os.path.basename(base_name)
        return None

    def remove_extension(self, file_path):
        base_name, _ = os.path.splitext(file_path)
        return base_name

if __name__ == '__main__':
    try:
        folder_path = sys.argv[1:][0]
        if not os.path.exists(folder_path):
            raise Exception('Path does not exist')
    except:
        folder_path = input('Path to folder: ')
        if not os.path.exists(folder_path):
            raise Exception('Path does not exist')
        
    try:
        if (sys.argv[1:][1]) == 'False':
            to_rename = False
        else: 
            to_rename = True
    except:
        to_rename = True


    renamer = FileRenamer(folder_path, to_rename)
    renamer.rename_files()