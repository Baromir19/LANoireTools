import struct
import os, sys

class UberPointerManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._read_file()
        self.file_size = self._get_file_size()
        self.main_block_pointer = self._read_uint32(0x8)
        self.pointers = []
        self.pointers_addresses = []
        self.pointers_blocks = []
        self.pointer_block_data_type = 0
        self.readed_addresses = set()
        self.unpack_data()

    def _read_file(self):
        with open(self.file_path, 'rb') as file:
            return file.read()

    def _get_file_size(self):
        return os.path.getsize(self.file_path)

    def _read_uint32(self, offset):
        return struct.unpack_from('<I', self.data, offset)[0]

    def _read_uint16(self, offset):
        return struct.unpack_from('<H', self.data, offset)[0]

    def unpack_data(self):
        list_size_offset = 0xC
        global_data_pointer = self.main_block_pointer # for blocks of data, fe ptm, dds. global pointer

        while True:
            pointer_list_size = self._read_uint16(list_size_offset)
            current_element = list_size_offset + 2
            current_pointer_address = 0

            if pointer_list_size:
                for _ in range(pointer_list_size):
                    current_element_value = self._read_uint16(current_element)
                    if current_element_value & 0x8000:
                        #if current_element % 2:
                        #    current_element += 1
                        current_element_data = self._read_uint32(current_element)
                        data_shift = (current_element_data & 0x80000000) | ((current_element_data & 0x80000000) >> 16)
                        current_pointer_address = data_shift ^ current_element_data
                        current_element += 4
                    else:
                        current_pointer_address += 4 * current_element_value
                        current_element += 2
                    
                    final_pointer = current_pointer_address + self.main_block_pointer # + global_data_pointer
                    self.pointers_addresses.append(final_pointer)
                    self.pointers.append(self._read_uint32(final_pointer) + global_data_pointer)
                    self.pointers_blocks.append(self.pointer_block_data_type)

            pointer_block_to_end_byte = current_element & 2
            pointer_block_end = current_element + pointer_block_to_end_byte

            if pointer_block_end + 6 >= self.main_block_pointer: # additional 4-byte data + 2-byte block size = 6 bytes 
                break

            self.pointer_block_data_type = self._read_uint32(pointer_block_end)
            pointer_to_shifted_value = 0x0 # pointer to data block, fe dds
            
            if pointer_to_shifted_value:
                global_data_pointer = self._read_uint32(pointer_to_shifted_value + 4)
            else:
                global_data_pointer = 0

            list_size_offset = pointer_block_end + 4

        return current_pointer_address

    def get_pointer_by_block(self, block_num: int):
        pointers_to_ret = []
        pointers_addresses_to_ret = []

        for i in range(len(self.pointers_blocks)):
            if self.pointers_blocks[i] == block_num:
                pointers_to_ret.append(self.pointers[i])
                pointers_addresses_to_ret.append(self.pointers_addresses[i])

        return pointers_to_ret, pointers_addresses_to_ret

    def get_vertex_positions_multiplier(self, pointers, pointers_addresses):
        results = []
        
        with open(self.file_path, 'rb') as file:
            for i in range(0, len(pointers), 2):  # 1st ptr is to beginning of the vertex block (buffer), 2nd -> indeces block
                pointer = pointers[i]
                address = pointers_addresses[i] - 0x14  # - 0x14 bytes for 3 float multipliers
                
                file.seek(address)
                data = file.read(12)
                if len(data) < 12:
                    continue
                
                values = struct.unpack('fff', data)
                results.append(values)
        
        return results

    def print_pointers(self):
        print(f"Main block: 0x{self.main_block_pointer:X}")
        print(f"Pointer count: {len(self.pointers)}")
        for i, pointer in enumerate(self.pointers):
            if not self.pointers_blocks[i]:
                print(f"Pointer {i}: 0x{pointer:X} (address: 0x{self.pointers_addresses[i]:X})")
            else:
                print(f"Pointer {i}: (DDS 0x{self.pointers_blocks[i]:X}) + 0x{pointer:X} (address: 0x{self.pointers_addresses[i]:X})")

    def print_pointers_values(self, to_float = False):
        combined = list(zip(self.pointers, self.pointers_addresses, self.pointers_blocks))
        sorted_combined = sorted(combined, key=lambda x: x[0])
        print('_______________________________\n')

        for pointer, address, block_type in sorted_combined:
            self.readed_addresses.add(address)

            if not block_type:
                next_addresses = [cpy_pointer for cpy_pointer, _, cpy_block_type in sorted_combined if not cpy_block_type and pointer < cpy_pointer]
                next_addresses += [cpy_address for _, cpy_address, _ in sorted_combined if pointer < cpy_address]
                next_addresses.append(self.file_size)
                next_address = min(next_addresses)

                bytes_between = self.data[pointer:next_address]
                values = struct.unpack('<' + 'I' * (len(bytes_between) // 4), bytes_between)
                print(f"Pointer 0x{pointer:04X}:", ' '.join(f"{value:08X}" if not to_float else f"{struct.unpack('<f', struct.pack('<I', value))[0]}" for value in values))

                self.readed_addresses.update(range(pointer, next_address, 4)) 

        #print("Read addresses:", sorted(self.readed_addresses))
        print('_______________________________\nAnother data:')

        unread_bytes = []
        for i in range(self.main_block_pointer, self.file_size, 4):
            if i not in self.readed_addresses:
                value = struct.unpack('<I', self.data[i:i+4])[0]
                if unread_bytes and i - unread_bytes[-1][0] > 4:
                    print(' '.join(f"{value:08X}" if not to_float else f"{struct.unpack('<f', struct.pack('<I', value))[0]}" for addr, value in unread_bytes))
                    unread_bytes = []
                unread_bytes.append((i, value))

        if unread_bytes:
            print(' '.join(f"{value:08X}" if not to_float else f"{struct.unpack('<f', struct.pack('<I', value))[0]}" for addr, value in unread_bytes))

def main():
    try:
        file_path = sys.argv[1:][0]
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')
    except:
        file_path = input('Path to file: ')
        if not os.path.exists(file_path):
            raise Exception('Path does not exist')

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        if sys.argv[1:][1].lower() == 'false':
            to_float = False
        else:
            to_float = True
    except:
        to_float = True

    try:
        unpacker = UberPointerManager(file_path)
        unpacker.print_pointers()
        unpacker.print_pointers_values(to_float) # maybe useless in future
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
