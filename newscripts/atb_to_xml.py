import os
import argparse
from xml.etree import ElementTree
from dictionaries import SIZE_DICT, TYPE_DICT, IS_SIZE_PTR_DICT, OBJECT_TYPES_DICTIONARY # type: ignore

import struct
import ctypes

BYTE_SIZE = 1
WORD_SIZE = 2
DWORD_SIZE = 4
QWORD_SIZE = 8

LANGUAGE_COUNT = 7

toPrintObjects = True # better comment 355-356

OBJECT_TYPES_DEFAULT = 'Object'

# BREAK_VALUE = 'exit'

ROOT_NAME = 'ATB'

read_filename = ''

# test, for print 2 related lists with sublists
def print_lists(names, values): 
    for name, value in zip(names, values):
        if isinstance(name, list) and isinstance(value, list):
            print_lists(name, value)
        else:
            print(f"{name}: {value}")

# bytes reader
def read_bytes(file, address, size):
    file.seek(address)
    return file.read(size)

# functions for finding sidnatures, deprecated
def find_signature(file, signature):
    file.seek(0)
    data = file.read()
    signature_bytes = bytes.fromhex(signature)
    start = 0
    addresses = []
    while start < len(data):
        pos = data.find(signature_bytes, start)
        if pos == -1:
            break
        addresses.append(pos)
        start = pos + 1
    return addresses

def find_signature_bytes(file, signature_bytes):
    file.seek(0)
    data = file.read()
    start = 0
    addresses = []
    while start < len(data):
        pos = data.find(signature_bytes, start)
        if pos == -1:
            break
        addresses.append(pos)
        start = pos + 1
    return addresses

def get_bin_element_size(file, string_size_address, bytes_size):
    string_size_bytes = read_bytes(file, string_size_address, bytes_size)
    return int.from_bytes(string_size_bytes, byteorder='little')

# reader for strings, uses size value
def get_string_value(file, string_value_address, string_size):
    string_bytes = read_bytes(file, string_value_address, string_size)
    return string_bytes.decode('utf-8')

# deprecated and useless
def get_table_string_count(file, string_count_address):
    return get_bin_element_size(file, string_count_address, WORD_SIZE)

# RETURNS THE STRING TABLES, deprecated
def get_table_strings(file, string_table_address, string_count, lang_count):
    strings_id = []
    strings_value = []

    current_string = 0
    current_address = string_table_address

    while current_string < string_count:
        current_address += 9

        string_id, current_address = get_string(file, current_address, WORD_SIZE) # to get the string id 
        strings_id.append(string_id)

        current_lang_string = 0

        while current_lang_string < lang_count: # get the string for every lang
            current_address += 5
            
            string_value, current_address = get_string(file, current_address, WORD_SIZE) 
            strings_value.append(string_value)
            current_lang_string += 1

        current_address += 1
        current_string += 1
    
    return strings_id, strings_value, current_address

# RETURNS STRING + POINTER AFTER STRING, deprecated
def get_string(file, substring_size_address, size_of_sizevar):
    data = file.read()
    substring_value = ""
    current_address = substring_size_address
    
    string_value_size = get_bin_element_size(file, substring_size_address, size_of_sizevar)
    substring_value_address = substring_size_address + size_of_sizevar
    current_address = substring_value_address + string_value_size

    if string_value_size > 0:
        substring_value = get_string_value(file, substring_value_address, string_value_size)

    return substring_value, current_address


def write_subelement_to_xml(father_element, element_name, text_value):
    name_element = ElementTree.SubElement(father_element, element_name) 
    name_element.text = text_value
    return name_element

# JUST WRITES TO FILE SUBSTRING (by lang), deprecated
def write_substring_to_xml(substring, string_id_element, current_lang):
    lang_value = ""
    
    match current_lang:
        case 0:
            lang_value = "Eng"
        case 1:
            lang_value = "Fra"
        case 2:
            lang_value = "Ger"
        case 3:
            lang_value = "Ita"
        case 4:
            lang_value = "Jap"
        case 5:
            lang_value = "Rus"
        case 6:
            lang_value = "Esp"

    write_subelement_to_xml(string_id_element, 'Substring' + lang_value, substring)

def save_xml(filename, tree):
    tree.write(filename)

def read_object_variable(file, data_address, father_element, is_array_element = False, known_variable_type = -1):
    result_value = None
    signature_value = b'\x00\x00\x00\x00'
    variable_type = None
    var_size = 0
    is_poly_empty = False

    if not is_array_element:
        var_size = int.from_bytes(read_bytes(file, data_address, BYTE_SIZE), byteorder='little')
        data_address += BYTE_SIZE
    else:
        var_size = known_variable_type

    # end of structure, object: additional 0 bit
    if var_size == 0:
        return True, data_address 

    if not is_array_element:
        variable_type = TYPE_DICT[var_size]
    else:
        variable_type = 'element'

    # array elements without signature
    if not is_array_element:
        signature_value = read_bytes(file, data_address, DWORD_SIZE)
        data_address += DWORD_SIZE # some signature, maybe 4 byte hash of variable name

    variable_name = None
    if signature_value in OBJECT_TYPES_DICTIONARY:
        variable_name = OBJECT_TYPES_DICTIONARY[signature_value]
    else:
        variable_name = '0x' + ''.join(format(byte, '02X') for byte in signature_value)


    real_size = SIZE_DICT[var_size]

    if IS_SIZE_PTR_DICT[var_size]: # CHECKING IS IT A STRING
        real_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little')

        if (real_size != 0xFFFF) and (real_size != 0x0000): 
            result_value, data_address = get_string(file, data_address, WORD_SIZE)
        else:
            data_address += WORD_SIZE
            result_value = "" 
            real_size = 0

        object_subelement = ElementTree.SubElement(father_element, variable_type, {'name': variable_name})
        object_subelement.text = result_value

    else:
        real_size = SIZE_DICT[var_size]
        result_value = read_bytes(file, data_address, real_size)
        data_address += real_size 

        if var_size == 0x46 or (var_size == 30 and int.from_bytes(result_value, byteorder='little')):
            object_value = '0x' + ''.join([f'{b:02x}' for b in result_value]) 

            object_subelement = ElementTree.SubElement(father_element, variable_type, {'name': variable_name})
            object_subelement.text = object_value

            data_address = read_object(file, data_address, object_subelement) # RECURSION FOR OBJECT

        elif var_size == 0x3C:
            array_type = int.from_bytes(read_bytes(file, data_address, BYTE_SIZE), byteorder='little')
            data_address += BYTE_SIZE
            array_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little')
            data_address += WORD_SIZE

            object_subelement = ElementTree.SubElement(father_element, variable_type, {'name': variable_name, 'elementType': TYPE_DICT[array_type]})

            data_address = read_array(file, data_address, array_size, array_type, object_subelement)

        elif var_size == 40:
            result_value = '0x' + ''.join([f'{b:02x}' for b in result_value])
        elif var_size == 30:
            result_value = '0x' + ''.join([f'{b:02x}' for b in result_value])
            is_poly_empty = True
        elif var_size == 10:
            result_value = ', '.join(map(str,struct.unpack('4f', result_value)))
        elif var_size == 9:
            result_value = '0x' + ''.join([f'{b:02x}' for b in result_value])
        elif var_size == 7:
            # print(signature_value)
            result_value = ', '.join(map(str,struct.unpack('16f', result_value)))
        elif var_size == 6:
            result_value = ', '.join(map(str,struct.unpack('2f', result_value)))
        elif var_size == 5:
            result_value = ', '.join(map(str,struct.unpack('3f', result_value)))
        elif var_size == 4:
            if (int.from_bytes(result_value, byteorder='little')):
                result_value = 'true'
            else:
                result_value = 'false'
        elif var_size == 3:
            result_value = struct.unpack('f', result_value)[0]
        elif var_size == 2:
            result_value = int.from_bytes(result_value, byteorder='little')
        elif var_size == 1:
            result_value = ctypes.c_int32(int.from_bytes(result_value, byteorder='little')).value 

        if var_size not in [60, 70, 30] or (var_size == 30 and is_poly_empty):
            
            object_subelement = ElementTree.SubElement(father_element, variable_type, {'name': variable_name})
            object_subelement.text = str(result_value)

    return False, data_address

def read_object(file, data_address, father_element): # this is a structure reader, at the end is '00' value

    while True:
        to_break, data_address = read_object_variable(file, data_address, father_element)

        if to_break:
            break

    return data_address

def read_array(file, data_address, array_size, array_type, father_element): 

    counter = 0

    if array_size:
        while counter < array_size:
            to_break, data_address = read_object_variable(file, data_address, father_element, True, array_type)
            counter += 1

    return data_address

def read_serialized_object(file, data_address, father_element):
    object_signature = read_bytes(file, data_address, DWORD_SIZE)
    data_address += DWORD_SIZE
    object_name, data_address = get_string(file, data_address, BYTE_SIZE)
    
    if toPrintObjects:
        print(object_name)

    object_type = None

    if object_signature in OBJECT_TYPES_DICTIONARY:
        object_type = OBJECT_TYPES_DICTIONARY[object_signature]
    else:
        object_type = OBJECT_TYPES_DEFAULT

    object_subelement = ElementTree.SubElement(father_element, object_type, {'name': object_name, 'object_signature': '0x' + ''.join(format(byte, '02X') for byte in object_signature)})

    counter = 0

    while True:
        to_break, data_address = read_object_variable(file, data_address, object_subelement)
        counter += 1

        if to_break: # variable_data == BREAK_VALUE:
            break

    subarray_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little') # TODO: ADD COUNT OF INCLUDING IF NOT ZERO
    data_address += WORD_SIZE # 2 reserved bytes before new object (including count)

    while subarray_size > 0:
        data_address = read_serialized_object(file, data_address, object_subelement)

        subarray_size -= 1

    return data_address

#                                                                               --- CODE START ---
parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs='?', help="File name")
args = parser.parse_args()

if not args.filename:
    read_filename = input("Enter file name: ")
else:
    read_filename = args.filename

if not os.path.isfile(read_filename):
    if os.path.isfile(read_filename + '.atb'):
        read_filename += '.atb'
    else:
        raise Exception('Wrong path')

string_table_signature = '3E80671C'
string_table_signature_bytes = bytes.fromhex(string_table_signature)
string_table_signature_size = len(string_table_signature_bytes)
bytes_string_table_size = BYTE_SIZE

object_container_sign = 'B664C176'
object_container_sign_bytes = bytes.fromhex(object_container_sign)
object_container_sign_size = len(object_container_sign_bytes)
bytes_object_container_size = BYTE_SIZE

actor_object_signature = '51FC4898'
actor_object_signature_bytes = bytes.fromhex(actor_object_signature)
actor_object_signature_size = DWORD_SIZE

conversation_template_signature = 'F4F07E78'
conversation_template_signature_bytes = bytes.fromhex(conversation_template_signature)
conversation_template_signature_size = DWORD_SIZE

metadata_signature = '5BF9F416' # unknown format of data... end of file for me
metadata_signature_bytes = bytes.fromhex(metadata_signature)
metadata_signature_size = DWORD_SIZE

current_data_address = 0

outfilename = read_filename
if '.atb' in outfilename:
    outfilename = outfilename.replace('.atb', '.xml')
else:
    outfilename += '.xml'

root = ElementTree.Element(ROOT_NAME, {'name': '', 'crc': '0', 'baseType': '', 'hierarchy': '', 'contentsLoadedByDefault': 'false'})

print(string_table_signature_bytes)

with open(read_filename, 'rb') as file:
    current_data_address += 0x4 # first 4 bytes is signauture of file type (41544204)

    container_element_count = int.from_bytes(read_bytes(file, current_data_address, WORD_SIZE), byteorder='little') # 2 bytes - count of containers (containers includes other containers..)
    print(container_element_count)

    current_data_address += WORD_SIZE
    current_container_element = 0

    while current_container_element < container_element_count: # READS THE CONTAINERS WITH DATA
        current_data_address = read_serialized_object(file, current_data_address, root) # HERE YOU CAN GET ARRAY OF DATA FOR FUTURE USING

        current_container_element += 1

    metadata_string = '0x' + ''.join(format(byte, '02X') for byte in file.read())
    # print(metadata_string)

    metadata_tree = ElementTree.SubElement(root, 'MetaData')
    metadata_tree.text = metadata_string

print('Ready!')

tree = ElementTree.ElementTree(root)
save_xml(outfilename, tree)
