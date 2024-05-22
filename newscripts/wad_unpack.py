import os, sys
import struct
from typing import BinaryIO

class WadExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.output_dir = 'entries\\' + os.path.basename(file_path) + '\\'
        
        if self.output_dir:
            os.makedirs(self.output_dir, exist_ok=True)

    def extract_files(self):
        with open(self.file_path, 'rb') as file:
            file.seek(4) # set cursor reader after magic bytes 
            file_count = int.from_bytes(file.read(4), byteorder='little')

            entries_information, names_table_offset = self._read_names_offset(file, file_count)

            for entry in range(file_count):
                entry_crc, entry_offset, entry_size = entries_information[entry].values()
                file.seek(entry_offset)
                entry_data = file.read(entry_size)

                file.seek(names_table_offset)
                entry_name_size = int.from_bytes(file.read(2), byteorder='little')
                entry_name = file.read(entry_name_size).decode()
                names_table_offset = file.tell()

                print(entry_name)

                output_file_path = self._sanitize_file_name(self.output_dir + entry_name)

                with open(output_file_path, 'wb') as output_file:
                    output_file.write(entry_data)

    def _read_names_offset(self, file: BinaryIO, file_count: int) -> int:
        file.seek(8 + 4 + (file_count - 1) * 12) # wad header + file crc + data offset for file
        (element_offset, element_size) = struct.unpack('<2I', file.read(struct.calcsize('<2I')))
        names_table_offset = element_offset + element_size

        file.seek(8)
        files_information = list()

        for file_num in range(file_count):
            file_crc, file_offset, file_size = struct.unpack('<3I', file.read(struct.calcsize('<3I')))
            
            file_information = {
                'crc32': file_crc,
                'offset': file_offset,
                'size': file_size
            }

            print(f'File {file_num} data on {file.tell():x}')
            files_information.append(file_information)

        return files_information, names_table_offset

    @staticmethod
    def _sanitize_file_name(file_name: str) -> str:
        sanitized_name = file_name.replace('/', '\\')
        os.makedirs(os.path.dirname(sanitized_name), exist_ok=True)

        return sanitized_name

if __name__ == '__main__':
    try:
        file_path = sys.argv[1:][0]
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')
    except:
        file_path = input('Path to folder: ')
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')

    extractor = WadExtractor(file_path)
    extractor.extract_files()