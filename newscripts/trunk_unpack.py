import os, sys
import struct
from typing import List, Dict, Tuple

class TrunkFileProcessor:
    def __init__(self, filename: str):
        self.filename = filename
        self.file_to_read = None
        self.texture_blocks_offsets: List[Dict[str, int]] = None
        self.entries_offsets: List[Dict[str, int]] = None

    def __enter__(self) -> 'TrunkFileProcessor':
        self.file_to_read = open(self.filename, 'rb')
        self.file_to_read.seek(4) # magic
        block_info_size = struct.unpack('<I', self.file_to_read.read(struct.calcsize('<I')))[0]
        self.texture_blocks_offsets = self.get_texture_block_offsets(block_info_size)
        table_size = struct.unpack('<I', self.file_to_read.read(struct.calcsize('<I')))[0]
        self.entries_offsets = self.get_table_offsets(table_size)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_to_read.close()

    def get_table_offsets(self, table_size: int) -> List[Dict[str, int]]:
        table_data = []
        for _ in range(table_size):
            crc_value, entry_size, entry_offset_start = struct.unpack('<3I', self.file_to_read.read(struct.calcsize('<3I')))
            row_data = {
                'crc32': crc_value,
                'entry_size': entry_size,
                'entry_start': entry_offset_start
            }
            table_data.append(row_data)
        return table_data

    def get_texture_block_offsets(self, blocks_size: int) -> List[Dict[str, int]]:
        texture_blocks = []
        for _ in range(blocks_size):
            block_offset_start, block_size = struct.unpack('<2I', self.file_to_read.read(struct.calcsize('<2I')))
            print(f'{block_offset_start:08x} has {block_size:08x} bytes ({(block_offset_start + block_size):08x})')
            texture_block = {
                'block_start': block_offset_start,
                'block_end': block_size
            }
            texture_blocks.append(texture_block)
        self.file_to_read.read(4)
        return texture_blocks

    def get_real_offset(self, entry_offset: int, blocks_table: List[Dict[str, int]]) -> int:
        if entry_offset % 0x10:
            blocks_table_index = (entry_offset % 0x10) - 1
            block_offset_start = blocks_table[blocks_table_index]['block_start']
            entry_offset_start = block_offset_start + entry_offset & 0xFFFFFFF0
            return entry_offset_start
        else:
            return entry_offset

    def process_data(self):
        mkdirSafe(self.filename + '_entries')
        for entry_offsets in self.entries_offsets:
            entry_start_offset = self.get_real_offset(entry_offsets['entry_start'], self.texture_blocks_offsets)
            entry_size = entry_offsets['entry_size']
            entry_crc = entry_offsets['crc32']
            print(f'Hash {entry_crc:08x} block from {entry_start_offset:08x} has {entry_size:08x} bytes')
            self.write_entries(entry_start_offset, entry_size, entry_crc)

    def write_entries(self, entry_offset: int, entry_size: int, entry_crc: int):
        try:
            with open(self.filename + '_entries' + f'\\0x{entry_crc:08x}', 'wb') as file_to_write:
                self.file_to_read.seek(entry_offset)
                entry_data = self.file_to_read.read(entry_size)
                file_to_write.write(entry_data)
        except OSError as e:
            print(e)

def mkdirSafe(dirs: str):
    try:
        print(dirs)
        os.makedirs(dirs)
    except OSError as e:
        print(e)

if __name__ == '__main__':
    try:
        file_path = sys.argv[1:][0]
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')
    except:
        file_path = input('Path to folder: ')
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')
        
    with TrunkFileProcessor(file_path) as processor:
        processor.process_data()