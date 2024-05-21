import os, sys
import xml.etree.ElementTree as ET
import struct

from dictionaries import SIZE_DICT, TYPE_DICT, IS_SIZE_PTR_DICT, OBJECT_TYPES_DICTIONARY

DIRECTORY = ''
FILE_FORMAT = '.atb.chunk'
REVERSE_TYPE_DICT = dict()
REVERSE_OBJECT_TYPES_DICTIONARY = dict()

def get_tree_root(xml_path):
    tree = ET.parse(xml_path)
    return tree.getroot()

def object_writer(file_write, element):
    crc32_value = element.get('object_signature')
    crc32_bytes = struct.pack('>I', int(crc32_value, 16))
    file_write.write(crc32_bytes)

    object_name = element.get('name')

    print(object_name) # if you want

    name_length = len(object_name)
    file_write.write(struct.pack('B%ds' % name_length, name_length, object_name.encode('ascii', 'ignore')))

    subobjects = sum(1 for subelement in element if (subelement.get('object_signature') is not None)) # test in future
    element_ending = struct.pack('<BH', 0, subobjects)
    object_elements = list(element)

    for subelement in object_elements:
        if subelement.get('object_signature') is not None:
            file_write.write(element_ending)
            element_ending = b''

        write_variable_data(file_write, subelement)

    file_write.write(element_ending)

def structure_writer(file_write, element):
    struct_elements = list(element)

    file_write.write(struct.pack('>I', int(element.text, 16))) # wrong endian in atb_to_xml?

    for subelement in struct_elements:
        write_variable_data(file_write, subelement)

    file_write.write(b'\x00')

def array_writer(file_write, element):
    array_elements = list(element)

    array_variable_type = int(REVERSE_TYPE_DICT.get(element.get('elementType'), None))
    array_variable_count = len(array_elements)

    file_write.write(struct.pack('<BH', array_variable_type, array_variable_count))

    for subelement in array_elements:
        write_variable_data(file_write, subelement, True, array_variable_type)

def write_variable_data(file_write, element, is_array_element = False, predefined_variable = 0):
    if element.get('object_signature') is not None: # RENAMe IN FUTURE TO CRC
        object_writer(file_write, element)
    elif element.tag in TYPE_DICT.values() or is_array_element:
        variable_type_code = 0

        if not is_array_element:
            variable_type_code = REVERSE_TYPE_DICT.get(element.tag, None)
            file_write.write(struct.pack('B', variable_type_code))
        else:
            variable_type_code = predefined_variable

        if not is_array_element:
            name_value = element.get('name')
            crc32_bytes = b''
            if name_value.startswith('0x'):
                crc32_bytes = struct.pack('>I', int(name_value, 16))
            else:
                crc32_bytes = REVERSE_OBJECT_TYPES_DICTIONARY.get(name_value, None)

            file_write.write(crc32_bytes)

        varible_text_value = element.text

        if (variable_type_code in (1, 2, 3, 4, 9, 40, 50)): # 1-8 bytes standart type values
            variable_byte_value = b''

            if variable_type_code in (9, 40, 50): # long, short, long
                value = int(varible_text_value, 16)

                if variable_type_code in (9, 50):
                    variable_byte_value = struct.pack('>Q', value)
                else:
                    variable_byte_value = struct.pack('>H', value)

            elif variable_type_code == 4: # bool
                if varible_text_value == 'true':
                    variable_byte_value = b'\x01'
                else:
                    variable_byte_value = b'\x00'

            elif variable_type_code == 3: # float
                variable_byte_value = struct.pack('<f', float(varible_text_value))
            elif variable_type_code == 2: # unsigned
                variable_byte_value = struct.pack('<I', int(varible_text_value))
            elif variable_type_code == 1: # signed
                variable_byte_value = struct.pack('<i', int(varible_text_value))

            file_write.write(variable_byte_value)

        elif (variable_type_code in (5, 6, 7, 10)): # special types (Vec, Mat)
            variable_byte_value = b''

            floats = list(map(float, varible_text_value.split(', ')))
            if variable_type_code == 5:
                variable_byte_value = struct.pack('3f', *floats)
            if variable_type_code == 6:
                variable_byte_value = struct.pack('2f', *floats)
            if variable_type_code == 7:
                variable_byte_value = struct.pack('16f', *floats)
            if variable_type_code == 10:
                variable_byte_value = struct.pack('4f', *floats)

            file_write.write(variable_byte_value)

        elif (variable_type_code in (8, 11)): # strings 
            if varible_text_value:
                string_variable_byte = varible_text_value.encode('utf-8', 'ignore')
                variable_byte_size = len(string_variable_byte)
                file_write.write(struct.pack('<H%ds' % variable_byte_size, variable_byte_size, string_variable_byte))
            else:
                file_write.write(b'\x00\x00')

        elif (variable_type_code in (30, 70)): # structures
            if (variable_type_code == 70 or (variable_type_code == 30 and int(varible_text_value, 16))):
                structure_writer(file_write, element)
            else:
                file_write.write(b'\x00\x00\x00\x00') # TO TEST

        elif variable_type_code == 60:
            array_writer(file_write, element)
        else:
            raise Exception('Unknown type')


    else:
        raise Exception('Unknown type: ' + element.tag)
    

def atb_packer(xml_file_path):
    global DIRECTORY
    global REVERSE_TYPE_DICT
    global REVERSE_OBJECT_TYPES_DICTIONARY

    DIRECTORY = os.path.dirname(xml_file_path) 
    root_tree = get_tree_root(xml_file_path)

    xml_filename = os.path.basename(xml_file_path)
    base_name = os.path.splitext(xml_filename)[0]

    atb_filename = base_name + FILE_FORMAT
    root_count = sum(1 for element in root_tree if element.tag != 'MetaData')

    with open(DIRECTORY + atb_filename, 'wb') as atb_file:
        magic_value = b'\x41\x54\x42\x04'
        header_value = struct.pack('<4sH', magic_value, root_count)

        atb_file.write(header_value)

        root_elements = list(root_tree)

        REVERSE_TYPE_DICT = {value: key for key, value in TYPE_DICT.items()}
        REVERSE_OBJECT_TYPES_DICTIONARY = {value: key for key, value in OBJECT_TYPES_DICTIONARY.items()}

        for elem in root_elements:
            if elem.tag == 'MetaData':
                metadata_text = elem.text

                if metadata_text.startswith('0x'):
                    metadata_text = metadata_text[2:]

                metadata_bytes = bytes.fromhex(metadata_text)
                atb_file.write(metadata_bytes)
                break

            write_variable_data(atb_file, elem)
        
    return True

# START
try:
    file_path = sys.argv[1:][0]
except:
    file_path = input('Path to folder: ')
    if not os.path.exists(file_path):
        raise Exception('Path does not exist')

if not os.path.exists(file_path):
    file_path = input('Path to folder: ')

if not os.path.exists(file_path):
    raise Exception('Path does not exist')

if (atb_packer(f'{file_path}')):
    print('Ready!')