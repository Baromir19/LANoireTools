import os
import argparse

def read_bytes(file, address, size):
    file.seek(address)
    return file.read(size)

def find_signature(file, signature):
    data = file.read()
    signature_bytes = bytes.fromhex(signature)
    start = 0
    addresses = []
    while start < len(data):
        pos = data.find(signature_bytes, start)
        if pos == -1:
            break
        #addresses.append(format(pos, "x"))
        addresses.append(pos)
        start = pos + 1
    return addresses

def find_signature_bytes(file, signature_bytes):
    data = file.read()
    start = 0
    addresses = []
    while start < len(data):
        pos = data.find(signature_bytes, start)
        if pos == -1:
            break
        #addresses.append(format(pos, "x"))
        addresses.append(pos)
        start = pos + 1
    return addresses

def get_bin_element_size(file, string_size_address, bytes_size):
    data = file.read()
    #string_size_address = signature_address + signature_size
    string_size_bytes = read_bytes(file, string_size_address, bytes_size)
    return int.from_bytes(string_size_bytes, byteorder='little')

def get_string_value(file, string_value_address, string_size):
    data = file.read()
    #string_value_address = signature_address + signature_size + 1
    string_bytes = read_bytes(file, string_value_address, string_size)
    return string_bytes.decode('utf-8')

def get_table_string_count(file, string_count_address):
    return get_bin_element_size(file, string_count_address, 2)

def get_table_strings(file, string_table_address, string_count, lang_count):
    data = file.read()
    strings_id = []
    strings_value = []

    current_string = 0
    current_address = string_table_address

    while current_string < string_count:
        current_address += 9
        # print(f'{current_address}')
        
        string_id_size = get_bin_element_size(file, current_address, 2)
        current_address += 2
        string_id = get_string_value(file, current_address, string_id_size)
        # print(f'{current_string}: {string_id}')
        strings_id.append(string_id)
        current_address += string_id_size

        current_lang_string = 0

        while current_lang_string < lang_count:
            current_address += 5
            
            string_value_size = get_bin_element_size(file, current_address, 2)
            current_address += 2

            if string_value_size > 0:
                string_value = get_string_value(file, current_address, string_value_size)
                # print(f'{current_lang_string}: {string_value}')
                strings_value.append(string_value)

            current_address += string_value_size
            current_lang_string += 1

        current_address += 1
        current_string += 1
    
    return strings_id, strings_value

def write_to_file(filepath, filename, string_value, set_formatted, start_value):
    # if filepath is 0, write to current folder
    if filepath == 0:
        filepath = ''
    full_path = os.path.join(filepath, filename)

    # is file exist, if not - create
    if not os.path.exists(full_path):
        open(full_path, 'w').close()

    if set_formatted:
        string_value = f'{start_value}"{string_value}"'

    with open(full_path, 'a', encoding='utf-8') as file:
        file.write(string_value + '\n')

def write_to_file(full_path, string_value, set_formatted, start_value):
    # is file exist, if not - create
    if not os.path.exists(full_path):
        open(full_path, 'w').close()

    if set_formatted:
        string_value = f'{start_value}"{string_value}"'

    with open(full_path, 'a', encoding='utf-8') as file:
        file.write(string_value + '\n')

def clear_file(filename):
    if os.path.exists(filename):
        open(filename, 'w').close()

# --- code start ---
# Parser creation
parser = argparse.ArgumentParser(description='Unpack ATB files.')
# Argument list
parser.add_argument('filename', help='The name of the file to unpack.')
# parser.add_argument('directory', help='The directory of the files to unpack.')
parser.add_argument('--outputpath', default='', help='The path to save the output files.')
parser.add_argument('--setformatted', action='store_true', help='Format the output strings.')
parser.add_argument('--addenter', action='store_true', help='Add an additional enter to the output.')

# Arguments parsing
args = parser.parse_args()

filename = args.filename
outfilename = args.outputpath if args.outputpath else filename
set_formatted = 1 if args.setformatted else 0
additional_enter = 1 if args.addenter else 0

# filename = 'test.atb'
string_table_signature = '3E80671C'
string_table_signature_bytes = bytes.fromhex(string_table_signature)
signature_size = len(string_table_signature_bytes)
bytes_stringtable_size = 1
#string_count_size = 2

LANGUAGE_COUNT = 7

# set_formatted = 0 # true
# additional_enter = 1

# outfilename = filename
if '.atb' in outfilename:
    outfilename = outfilename.replace('.atb', '.txt')
else:
    outfilename += '.txt'

clear_file(outfilename)

with open(filename, 'rb') as file:
    addresses = find_signature_bytes(file, string_table_signature_bytes)
    print(f'Signature addresses: {addresses}')
    for address in addresses:
        size_offset = address + signature_size
        
        string_size = get_bin_element_size(file, size_offset, bytes_stringtable_size)
        string_value = get_string_value(file, size_offset + bytes_stringtable_size, string_size)
        
        if additional_enter:
                    write_to_file(outfilename, '\n', 0, '')
                    
        write_to_file(outfilename, string_value, set_formatted, 't')

        substring_count_offset = size_offset + bytes_stringtable_size + string_size + 6
        substring_count = get_table_string_count(file, substring_count_offset)

        print(f'String table in {address}: ({string_size}) {string_value} have {substring_count} substrings')

        strings_id, strings_value = get_table_strings(file, substring_count_offset + 2, substring_count, LANGUAGE_COUNT)

        for i in range(len(strings_id)):
            if additional_enter:
                    write_to_file(outfilename, '', 0, '')
                    
            write_to_file(outfilename, strings_id[i], set_formatted, 'i')
            substring_values = strings_value[i*7 : (i+1)*7]
            for substring in substring_values:
                write_to_file(outfilename, substring, set_formatted, 's')
