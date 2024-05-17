import sys, os, errno
import array
from struct import *
import zlib
import xml.etree.ElementTree as ET

entry_xml_root = None
entry_xml_segments = None

entries_dir = None

def align(x, a):
    return (x + (a - 1)) & ~(a - 1)

def mkdirSafe(dirs):
    try:
        os.makedirs(dirs)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

class BigArchive:
    class Entry:
        def __init__(self):
            self.hash = None
            self.offset = None
            self.size1 = None
            self.size2 = None
            self.size3 = None

    class Chunk:
        def __init__(self):
            self.offset = None
            self.size = None
            self.flags = None
            self.size_coeff = None

    def __init__(self, file, endianness, file_name):
        self.endianness = endianness
        self.file = file
        self.file_size = None
        self.entries = None
        self.file_name = file_name

        current_pos = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        self.file_size = self.file.tell()
        self.file.seek(current_pos)
        self.file.seek(self.file_size - calcsize('<I'))

        self.file_table_offset = self.file_size - unpack('<I', self.file.read(calcsize('<I')))[0]
        self.file.seek(self.file_table_offset)

        (archive_type, num_entries) = unpack('<2I', self.file.read(calcsize('<2I')))
        if archive_type != 3:
            print(f'Unsupported archive type {archive_type}')
            return

        entry_xml_table = ET.SubElement(entry_xml_root, 'table', attrib={'archive_type': f'{archive_type}', 'num_entries': f'{num_entries}'}) # num_entries is necessary, since their number can be 0

        self.entries = []
        for i in range(num_entries):
            entry = self.Entry()

            (entry.hash, entry_offset, entry.size1, entry.size2, entry.size3) = unpack(self.endianness + '5I', self.file.read(calcsize(self.endianness + '5I')))
            entry_offset_lo = entry_offset << 4
            entry_offset_hi = entry_offset >> 28
            entry.offset = entry_offset_lo
            # size3 for compressed segs

            entry_xml_table_row = ET.SubElement(entry_xml_table, 'row', attrib={'hash': f'0x{entry.hash:08x}', 'offset': f'0x{entry.offset:08x}'})
            ET.SubElement(entry_xml_table_row, 'size1').text = f'{entry.size1}'
            ET.SubElement(entry_xml_table_row, 'size2').text = f'{entry.size2}'
            ET.SubElement(entry_xml_table_row, 'size3').text = f'{entry.size3}'

            self.entries.append(entry)

    def dumpEntry(self, entry, data):
        entry_dir = f'entries/{self.file_name}'
        mkdirSafe(entry_dir)
        with open(f'{entry_dir}/0x{entry.hash:08x}', 'wb') as out_file:
            out_file.write(data)

    def processSingle(self, entry):
        size = entry.size3
        if size == 0:
            size = entry.size1
        self.file.seek(entry.offset)
        data = self.file.read(size)
        self.dumpEntry(entry, data)

        # 1 case indicates that the segment is proceed with 1 chunk (without multithreading?) 
        entry_xml_segment = ET.SubElement(entry_xml_segments, 'segment', attrib={'hash': f'0x{entry.hash:08x}', 'case': '1'})

    def processMulti(self, entry):
        self.file.seek(entry.offset)
        (magic, type, num_chunks, u0, u1, u2, u3) = unpack(self.endianness + 'I2H4B', self.file.read(calcsize(self.endianness + 'I2H4B')))
        print(f'\tType: {type}')
        print(f'\tNum chunks: {num_chunks}')
        print(f'\tUnknown: {u0} {u1} {u2} {u3}')
        data_offset = align(self.file.tell() + u0 * calcsize(self.endianness + 'I') + num_chunks * calcsize(self.endianness + '2H'), 16)

        # 2 case indicates that the segment is proceed with many chunks (with multithreading?) 
        entry_xml_segment = ET.SubElement(entry_xml_segments, 'segment', attrib={'hash': f'0x{entry.hash:08x}', 'type': f'{type}', 'u0': f'{u0}', 'u1': f'{u1}', 'u2': f'{u2}', 'u3': f'{u3}', 'case': '2'})

        uobjs = []
        for i in range(u0):
            uobj = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
            uobjs.append(uobj)

        chunks = []
        for i in range(num_chunks):
            chunk = self.Chunk()

            (chunk.size, chunk.flags, chunk.size_coeff) = unpack(self.endianness + 'H2B', self.file.read(calcsize(self.endianness + 'H2B')))

            chunk.offset = data_offset
            chunk.size += 0x10000 * chunk.size_coeff
            data_offset += chunk.size
            chunks.append(chunk)

        data = b''

        for i in range(len(uobjs)):
            uobj = uobjs[i]

            print(f'\tObject {i}:')
            print(f'\t\tData: {uobj}')
            ET.SubElement(entry_xml_segment, 'object').text = uobj
        print('')

        for i in range(len(chunks)):
            chunk = chunks[i]

            print(f'\tChunk {i}:')
            print(f'\t\tOffset: {chunk.offset}')
            print(f'\t\tSize: {chunk.size}')
            print(f'\t\tFlags: 0x{chunk.flags:02x}')
            print(f'\t\tSize coeff: {chunk.size_coeff}')

            # size & offset probably useless
            entry_xml_chunk = ET.SubElement(entry_xml_segment, 'chunk', attrib={'flags': f'0x{chunk.flags:02x}', 'size_coefficient': f'{chunk.size_coeff}', 'size': f'{chunk.size}', 'offset': f'{chunk.offset}'})

            self.file.seek(chunk.offset)
            if chunk.flags & 0x10:
                data += zlib.decompress(self.file.read(chunk.size), -15)
            else:
                data += self.file.read(chunk.size)

        self.dumpEntry(entry, data)

    def unpack(self):
        global entry_xml_segments, entries_dir
        entry_xml_segments = ET.SubElement(entry_xml_root, 'segments')

        num_segments = 0
        entries_dir = f'entries/{self.file_name}'
        mkdirSafe(entries_dir)
        with open(f'{entries_dir}/entries.txt', 'w') as entries_list_file:
            if not self.entries:
                offset = 0

                while offset < self.file_table_offset:
                    self.file.seek(offset)

                    magic = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
                    self.file.seek(-calcsize(self.endianness + 'I'), os.SEEK_CUR)
                    if magic == unpack_from(b'>I', b'segs')[0]:
                        (magic, type, num_chunks, u0, u1, u2, u3) = unpack(self.endianness + 'I2H4B', self.file.read(calcsize(self.endianness + 'I2H4B')))
                        print(f'\tType: {type}')
                        print(f'\tNum chunks: {num_chunks}')
                        print(f'\tUnknown: {u0} {u1} {u2} {u3}')
                        data_offset = align(self.file.tell() + u0 * calcsize(self.endianness + 'I') + num_chunks * calcsize(self.endianness + '2H'), 16)

                        # num_chunks, u1-u3 probably useless; 0 case indicates that the segment is proceed without a entries table 
                        entry_xml_segment = ET.SubElement(entry_xml_segments, 'segment', attrib={'hash': f'0x{entry.hash:08x}', 'type': f'{type}', 'u0': f'{u0}', 'u1': f'{u1}', 'u2': f'{u2}', 'u3': f'{u3}', 'case': '0'})

                        uobjs = []
                        for i in range(u0):
                            uobj = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
                            uobjs.append(uobj)

                        chunks = []
                        chunks_total_size = 0
                        for i in range(num_chunks):
                            chunk = self.Chunk()

                            (chunk.size, chunk.flags, chunk.size_coeff) = unpack(self.endianness + 'H2B', self.file.read(calcsize(self.endianness + 'H2B')))

                            chunk.offset = data_offset
                            chunk.size += 0x10000 * chunk.size_coeff
                            chunks_total_size += chunk.size
                            data_offset += chunk.size
                            chunks.append(chunk)

                        data = b''

                        for i in range(len(uobjs)):
                            uobj = uobjs[i]

                            print(f'\tObject {i}:')
                            print(f'\t\tData: {uobj}')
                            ET.SubElement(entry_xml_segment, 'object').text = uobj
                        print('')

                        for i in range(len(chunks)):
                            chunk = chunks[i]

                            print(f'\tChunk {i}:')
                            print(f'\t\tOffset: {chunk.offset}')
                            print(f'\t\tSize: {chunk.size}')
                            print(f'\t\tFlags: 0x{chunk.flags:02x}')
                            print(f'\t\tSize coeff: {chunk.size_coeff}')

                            # size & offset probably useless
                            entry_xml_chunk = ET.SubElement(entry_xml_segment, 'chunk', attrib={'flags': f'0x{chunk.flags:02x}', 'size_coefficient': f'{chunk.size_coeff}', 'size': f'{chunk.size}', 'offset': f'{chunk.offset}'})

                            self.file.seek(chunk.offset)
                            if chunk.flags & 0x10:
                                data += zlib.decompress(self.file.read(chunk.size), -15)
                            else:
                                data += self.file.read(chunk.size)
                        print(f'Total size: {chunks_total_size}')

                        entry_dir = f'segments/{self.file_name}'
                        mkdirSafe(entry_dir)
                        with open(f'{entry_dir}/{num_segments:06d}', 'wb') as fout:
                            fout.write(data)

                        while self.file.tell() + 16 < self.file_table_offset:
                            padding = self.file.read(16)
                            if padding != b'X' * 16 and padding != b'\x00' * 16:
                                self.file.seek(-16, os.SEEK_CUR)
                                break
                        offset = self.file.tell()

                        print(f'seg {num_segments}: {data_offset} -> {offset} ::: {offset - data_offset}')
                        num_segments += 1
                    else:
                        print('DAMN!!!!!!!!!!!!')
                print('')

            for i in range(len(self.entries)):
                entry = self.entries[i]

                entries_list_file.write(f'0x{entry.hash:08x}\n')
                
                self.file.seek(entry.offset)
                magic = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
                self.file.seek(-calcsize(self.endianness + 'I'), os.SEEK_CUR)
                if magic == unpack_from(b'>I', b'segs')[0]:
                    print('processing multi...')
                    print(f'\tHash: 0x{entry.hash:08x}')
                    print(f'\tOffset: {entry.offset}')
                    print(f'\tSize1: {entry.size1}')
                    print(f'\tSize2: {entry.size2}')
                    print(f'\tSize3: {entry.size3}')
                    self.processMulti(entry)
                else:
                    print('processing single...')
                    print(f'\tHash: 0x{entry.hash:08x}')
                    print(f'\tOffset: {entry.offset}')
                    print(f'\tSize1: {entry.size1}')
                    print(f'\tSize2: {entry.size2}')
                    print(f'\tSize3: {entry.size3}')
                    self.processSingle(entry)
                print('')

def processFile(file_name):
    global entry_xml_root

    endianness = None
    if file_name.endswith('.pc'):
        endianness = '<'
    elif file_name.endswith('.ps3'):
        endianness = '>'
    elif file_name.endswith('.360'):
        print('Xbox 360 format is not supported for now')
        return
    else:
        print('Unknown format')
        return

    entry_xml_root = ET.Element('root', attrib={'endianness': endianness, 'file_name': os.path.basename(file_name)})

    with open(file_name, 'rb') as file:
        try:
            arc = BigArchive(file, endianness, os.path.basename(file_name))
            arc.unpack()
        except EOFError:
            print('Failed open file')
            return

mkdirSafe('segments')
list(map(lambda x: processFile(x) if os.path.exists(x) else None, sys.argv[1:]))

tree = ET.ElementTree(entry_xml_root)
tree.write(f'{entries_dir}/entries.xml')