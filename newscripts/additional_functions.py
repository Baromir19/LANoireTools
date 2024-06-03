from dictionaries import CRC32_KEY
import zlib

# Get hash value from string (file path. The hash value can be obtained from the name of the entry files (obtained from BigPC Unpacker))
def file_path_hash(file_path_value): 
    print('{} => 0x{:08x}'.format(file_path_value, zlib.crc32(file_path_value.encode()) & 0xffffffff))

def get_crc_from_string(stringValue: str) -> int:
    stringValue = stringValue.lower()

    result = 0xFFFFFFFF

    for i in range(len(stringValue)):
        symbol = ord(stringValue[i])

        result = CRC32_KEY[(result & 0xFF) ^ symbol] ^ (result >> 8)

    return ~(result & 0xFFFFFFFF) & 0xFFFFFFFF

# Loop that I use to quickly write dictionaries that are based on a name with XML
def convert_to_dictionary():
    my_bytes = list()
    while True:
        input_string = input("Input': ")
        if input_string == '0' or input_string == '':
            for single_string in my_bytes:
                print(single_string)

            my_bytes = list()
        elif input_string == '9':
            break
        else:
            try:
                index = input_string.find('0x')
                input_string = input_string[(index + 2):]
                input_string = input_string[:-1]
                pairs = [input_string[i:i+2] for i in range(0, len(input_string), 2)]
                input_string = "\\x".join(pairs)
                input_string = f"b'\\x{input_string}': '',"
                my_bytes.append(input_string)
                #print()
            except ValueError:
                print("Error")