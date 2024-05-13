# import os
# import argparse
# from xml.etree import ElementTree

import struct
import ctypes

BYTE_SIZE = 1
WORD_SIZE = 2
DWORD_SIZE = 4
QWORD_SIZE = 8

LANGUAGE_COUNT = 7

toPrintObjects = False # if you want to print something in console.. just uncomment 314-315

# as integer 1, 2 (unsigned), 9 (0x)
# as bool 4
# as float pointed 3, 5, 6, 7, 10
# as string 8, 11
SIZE_DICT = {
    1: 0x4, # INT
    2: 0x4, # unsigned int
    3: 0x4, # FLOAT
    4: 0x1, # BOOL
    5: 0xC, # its Vec3
    6: 0x8, # offset, uses 8 bytes?
    7: 0x40, # m256, using float
    8: 0x2, # STRING, SHOWS, HOW MANY STRING IT HAVE
    9: 0x8, # uint64
    10: 0x10, # m128, maybe array of 4 int
    11: 0x2, # substring in string table
    30: 0x4, # idk
    40: 0x2, # its object, i think, maybe it shows size of object or somehting? Pointer (Unscoped) to type -> %s
    50: 0x8, # long again, %u,%u format
    60: 0x0, # container of element
    70: 0x4 # ARRAY?? null value in end
}

TYPE_DICT = {
    1: 'int32',
    2: 'uint32', # unsigned int
    3: 'float', 
    4: 'bool', 
    5: 'Vec3', # uknown type, but object include 'Offset'? Vec3.
    6: 'Vec2', # uknown 8-byte type, but object include 'Offset', Vec2.
    7: 'Mat4', # uses 4*4 _m128, every float. In main name="Transform"
    8: 'AString', # string 
    9: 'uint64',
    10: 'Vec4',
    11: 'UString', #substring
    30: 'PolyPtr', # includes 4 bytes, if it isnt zero, then its object
    40: 'Link', # unknown type, maybe its string? its FFFF or 02/03/05 etc... 2 bytes, WeakRef<ExposedObject>
    50: 'Bitfield', # idk, maybe its long (exactly not uses float point)
    60: 'Array', # creates array of next element, uses predestined size
    70: 'Structure' # with many types
}

IS_SIZE_PTR_DICT = {
    1: 0, 
    2: 0,
    3: 0,
    4: 0,
    5: 0, 
    6: 0,
    7: 0, 
    8: 0, 
    8: 1,
    10: 0,
    11: 1,
    30: 0, 
    40: 0,
    50: 0,
    60: 0,
    70: 0
}

BASE_TYPE_DICT = {
    0x1: 'Object',
    0x2: 'Structure',
    0x4: 'Collection',
    0x8: 'MetaData',
    0x10: 'PolymorphicStructure'
}

BREAK_VALUE = 'exit'

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
    #data = file.read()
    string_size_bytes = read_bytes(file, string_size_address, bytes_size)
    return int.from_bytes(string_size_bytes, byteorder='little')

# reader for strings, uses size value
def get_string_value(file, string_value_address, string_size):
    #data = file.read()
    string_bytes = read_bytes(file, string_value_address, string_size)
    return string_bytes.decode('utf-8')

# deprecated and useless
def get_table_string_count(file, string_count_address):
    return get_bin_element_size(file, string_count_address, WORD_SIZE)

# RETURNS THE STRING TABLES, deprecated
def get_table_strings(file, string_table_address, string_count, lang_count):
    #data = file.read()
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
    name_element = ''#ElementTree.SubElement(father_element, element_name) # delete comment for xml
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

def read_object_variable(file, data_address, is_array_element = False, known_variable_type = -1):
    result_value = None
    signature_value = None
    variable_type = None
    var_size = 0

    if not is_array_element:
        var_size = int.from_bytes(read_bytes(file, data_address, BYTE_SIZE), byteorder='little')
        data_address += BYTE_SIZE
    else:
        var_size = known_variable_type

    # end of object: additional 0 bit
    if var_size == 0:
        return BREAK_VALUE, 0, 0, data_address

    variable_type = TYPE_DICT[var_size]

    # array elements without signature
    if not is_array_element:
        signature_value = int.from_bytes(read_bytes(file, data_address, DWORD_SIZE), byteorder='little') 
        data_address += DWORD_SIZE # some signature, maybe 4 byte hash of variable name
    else:
        signature_value = None

    real_size = SIZE_DICT[var_size]

    if IS_SIZE_PTR_DICT[var_size]: # CHECK IS IT STRING OR NOT
        real_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little')

        if (real_size != 0xFFFF) and (real_size != 0x0000): 
            result_value, data_address = get_string(file, data_address, WORD_SIZE)
        else:
            data_address += WORD_SIZE
            result_value = "" 
            real_size = 0

    else:
        real_size = SIZE_DICT[var_size]
        result_value = read_bytes(file, data_address, real_size)
        data_address += real_size 

        if var_size == 0x46 or (var_size == 30 and int.from_bytes(result_value, byteorder='little')):
            object_value = '0x' + ''.join([f'{b:02x}' for b in result_value]) # int.from_bytes(result_value, byteorder='little')
            object_signature = signature_value
            object_type = variable_type
            result_value = list()
            signature_value = list()
            variable_type = list()

            result_value, signature_value, variable_type, data_address = read_object(file, data_address) # RECURSION FOR OBJECT
            result_value.insert(0, object_value)
            signature_value.insert(0, object_signature)
            variable_type.insert(0, object_type)

        elif var_size == 0x3C:
            array_signature = signature_value
            type_of_array = variable_type
            result_value = list()
            signature_value = list()
            variable_type = list()

            array_type = int.from_bytes(read_bytes(file, data_address, BYTE_SIZE), byteorder='little')
            data_address += BYTE_SIZE
            array_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little')
            data_address += WORD_SIZE

            result_value, signature_value, variable_type, data_address = read_array(file, data_address, array_size, array_type)
            result_value.insert(0, array_size)
            signature_value.insert(0, array_signature)
            variable_type.insert(0, type_of_array)
        elif var_size == 40:
            result_value = '0x' + ''.join([f'{b:02x}' for b in result_value])
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
            result_value = ctypes.c_int32(int.from_bytes(result_value, byteorder='little')).value #int.from_bytes(result_value, byteorder='little') # do signed...
            # print(result_value)

    # print(result_value)

    return result_value, signature_value, variable_type, data_address

def read_object(file, data_address): # its object
    result_array = list()
    type_array = list()
    signature_array = list()

    while True:
        result_value, variable_signature, variable_type, data_address = read_object_variable(file, data_address)

        if result_value == BREAK_VALUE:
            break

        result_array.append(result_value)
        type_array.append(variable_type)
        signature_array.append(variable_signature)
    return result_array, signature_array, type_array, data_address

def read_array(file, data_address, array_size, array_type): # TODO: IF ARRAY IS EMPTY -> ADD NULL VALUE + TYPE (for type detection in future)
    result_array = list()
    type_array = list()
    signature_array = list()

    counter = 0

    if array_size:
        while counter < array_size:
            result_value, variable_signature, variable_type, data_address = read_object_variable(file, data_address, True, array_type)
            result_array.append(result_value)
            type_array.append(variable_type)
            signature_array.append(variable_signature)
            counter += 1
    else:
        result_array.append(None)
        type_array.append(TYPE_DICT[array_type])
        signature_array.append(None)


    return result_array, signature_array, type_array, data_address

def read_serialized_object(file, data_address):
    object_signature = read_bytes(file, data_address, DWORD_SIZE)
    # toPrint = 23
    # res = (int.from_bytes((object_signature), byteorder='little') >> toPrint) & 0b11111
    # print(f'{int.from_bytes((object_signature), byteorder='little'):X}, {data_address:x}, {res:x}')

    data_address += DWORD_SIZE

    object_name, data_address = get_string(file, data_address, BYTE_SIZE)
    
    #if toPrintObjects:
    #    print(object_name)
    
    counter = 0

    data_array = list() # object values
    type_array = list() # just for type for xml
    signature_array = list() # FOR DETECTION NAME OF VARIABLE. As i know 4 bytes of sign is like hash of name of type (object)

    while True:
        variable_data, variable_signature, variable_type, data_address = read_object_variable(file, data_address)
        counter += 1

        if variable_data == BREAK_VALUE:
            break

        data_array.append(variable_data)
        type_array.append(variable_type)
        signature_array.append(variable_signature)

    type_object = object_name # 'serialized'
    data_array.insert(0, type_object)
    type_array.insert(0, type) # idk, its object with serialized values so
    signature_array.insert(0, object_signature)

    subarray_size = int.from_bytes(read_bytes(file, data_address, WORD_SIZE), byteorder='little') # TODO: ADD COUNT OF INCLUDING IF NOT ZERO
    data_address += WORD_SIZE # 2 reserved bytes before new object (including count)

    #print(data_array)
    #print(type_array)
    #print(signature_array)
    #print_lists(type_array, data_array)

    while subarray_size > 0:
        subobject_data, subobject_type, subobject_signature, data_address = read_serialized_object(file, data_address)

        data_array.append(subobject_data)
        type_array.append(subobject_type)
        signature_array.append(subobject_signature)

        subarray_size -= 1

    return data_array, type_array, signature_array, data_address

#                                                                               --- CODE START ---
filename = 'test.atb'

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

outfilename = filename
if '.atb' in outfilename:
    outfilename = outfilename.replace('.atb', '.xml')
else:
    outfilename += '.xml'

# root = ElementTree.Element("ATB")

with open(filename, 'rb') as file:
    # DEPRECATED
    # containers_address = find_signature_bytes(file, object_container_sign_bytes) # FIND CONTAINTERS ADDRESS, remove later
    # metadata_address = find_signature_bytes(file, metadata_signature_bytes)[0] - 3
    # print(f'{metadata_address:x}')

    current_data_address += 0x4 # first 4 bytes is signauture of file type (41544204)

    container_element_count = int.from_bytes(read_bytes(file, current_data_address, WORD_SIZE), byteorder='little') # 2 bytes - count of containers (containers includes other containers..)
    print(container_element_count)

    current_data_address += WORD_SIZE
    current_container_element = 0

    while current_container_element < container_element_count: # READS THE CONTAINERS WITH DATA
        next_signature_value = read_bytes(file, current_data_address, 4)

        data_array, type_array, signature_array, current_data_address = read_serialized_object(file, current_data_address) # HERE YOU CAN GET ARRAY OF DATA FOR FUTURE USING

        current_container_element += 1
        # print(current_container_element)

    metadata_string = '0x' + ''.join(format(byte, '02X') for byte in file.read())
    print(metadata_string)

print('Ready')
# tree = ElementTree.ElementTree(root)
# save_xml(outfilename, tree)
