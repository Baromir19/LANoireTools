import sys, os, errno
import array
from struct import *
import zlib

def align(x, a):
	return (x + (a - 1)) & ~(a - 1);

def mkdirSafe(dirs):
	try:
		os.makedirs(dirs)
	except OSError, e:
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

	def __init__(self, file, endianness):
		self.endianness = endianness
		self.file = file
		self.file_size = None
		self.entries = None

		current_pos = self.file.tell()
		self.file.seek(0, os.SEEK_END)
		self.file_size = self.file.tell()
		self.file.seek(current_pos)
		self.file.seek(self.file_size - calcsize('<I'))

		self.file_table_offset = self.file_size - unpack('<I', self.file.read(calcsize('<I')))[0];
		self.file.seek(self.file_table_offset)

		(archive_type, num_entries) = unpack('<2I', self.file.read(calcsize('<2I')))
		if archive_type != 3:
			print 'Unsupported archive type %d' % archive_type
			return

		self.entries = []
		for i in xrange(num_entries):
			entry = self.Entry()

			(entry.hash, entry_offset, entry.size1, entry.size2, entry.size3) = unpack(self.endianness + '5I', self.file.read(calcsize(self.endianness + '5I')))
			entry_offset_lo = entry_offset << 4
			entry_offset_hi = entry_offset >> 28
			entry.offset = entry_offset_lo
			# size3 for compressed segs

			self.entries.append(entry)

	def dumpEntry(self, entry, data):
		with open('entries/0x%08x' % entry.hash, 'wb') as out_file:
			out_file.write(data)

	def processSingle(self, entry):
		size = entry.size3
		if size == 0:
			size = entry.size1
		self.file.seek(entry.offset)
		data = self.file.read(size)
		self.dumpEntry(entry, data)

	def processMulti(self, entry):
		self.file.seek(entry.offset)
		(magic, type, num_chunks, u0, u1, u2, u3) = unpack(self.endianness + 'I2H4B', self.file.read(calcsize(self.endianness + 'I2H4B')))
		print '\tType: %d' % type
		print '\tNum chunks: %d' % num_chunks
		print '\tUnknown: %d %d %d %d' % (u0, u1, u2, u3)
		data_offset = align(self.file.tell() + u0 * calcsize(self.endianness + 'I') + num_chunks * calcsize(self.endianness + '2H'), 16)

		uobjs = []
		for i in xrange(u0):
			uobj = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
			uobjs.append(uobj)

		chunks = []
		for i in xrange(num_chunks):
			chunk = self.Chunk()

			(chunk.size, chunk.flags, chunk.size_coeff) = unpack(self.endianness + 'H2B', self.file.read(calcsize(self.endianness + 'H2B')))

			chunk.offset = data_offset
			chunk.size += 0x10000 * chunk.size_coeff
			data_offset += chunk.size
			chunks.append(chunk)

		data = ''

		for i in xrange(len(uobjs)):
			uobj = uobjs[i]

			print '\tObject %d:' % i
			print '\t\tData: %d' % uobj
		print ''

		for i in xrange(len(chunks)):
			chunk = chunks[i]

			print '\tChunk %d:' % i
			print '\t\tOffset: %d' % chunk.offset
			print '\t\tSize: %d' % chunk.size
			print '\t\tFlags: 0x%02x' % (chunk.flags)
			print '\t\tSize coeff: %d' % (chunk.size_coeff)

			self.file.seek(chunk.offset)
			if chunk.flags & 0x10:
				data += zlib.decompress(self.file.read(chunk.size), -15)
			else:
				data += self.file.read(chunk.size)

		self.dumpEntry(entry, data)

	def unpack(self):
		num_segments = 0
		with open('entries.txt', 'w') as entries_list_file:
			if not self.entries:
				offset = 0
				
				while offset < self.file_table_offset:
					self.file.seek(offset)

					magic = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
					self.file.seek(-calcsize(self.endianness + 'I'), os.SEEK_CUR)
					if magic == unpack_from('>I', 'segs')[0]:
						(magic, type, num_chunks, u0, u1, u2, u3) = unpack(self.endianness + 'I2H4B', self.file.read(calcsize(self.endianness + 'I2H4B')))
						print '\tType: %d' % type
						print '\tNum chunks: %d' % num_chunks
						print '\tUnknown: %d %d %d %d' % (u0, u1, u2, u3)
						data_offset = align(self.file.tell() + u0 * calcsize(self.endianness + 'I') + num_chunks * calcsize(self.endianness + '2H'), 16)

						uobjs = []
						for i in xrange(u0):
							uobj = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
							uobjs.append(uobj)

						chunks = []
						chunks_total_size = 0
						for i in xrange(num_chunks):
							chunk = self.Chunk()

							(chunk.size, chunk.flags, chunk.size_coeff) = unpack(self.endianness + 'H2B', self.file.read(calcsize(self.endianness + 'H2B')))

							chunk.offset = data_offset
							chunk.size += 0x10000 * chunk.size_coeff
							chunks_total_size += chunk.size
							data_offset += chunk.size
							chunks.append(chunk)

						data = ''

						for i in xrange(len(uobjs)):
							uobj = uobjs[i]

							print '\tObject %d:' % i
							print '\t\tData: %d' % uobj
						print ''

						for i in xrange(len(chunks)):
							chunk = chunks[i]

							print '\tChunk %d:' % i
							print '\t\tOffset: %d' % chunk.offset
							print '\t\tSize: %d' % chunk.size
							print '\t\tFlags: 0x%02x' % (chunk.flags)
							print '\t\tSize coeff: %d' % (chunk.size_coeff)

							self.file.seek(chunk.offset)
							if chunk.flags & 0x10:
								data += zlib.decompress(self.file.read(chunk.size), -15)
							else:
								data += self.file.read(chunk.size)
						print 'Total size: %d' % chunks_total_size

						with open('segments/%06d' % num_segments, 'wb') as fout:
							fout.write(data)

						while self.file.tell() + 16 < self.file_table_offset:
							padding = self.file.read(16)
							if padding != 'X' * 16 and padding != '\x00' * 16:
								self.file.seek(-16, os.SEEK_CUR)
								break
						offset = self.file.tell()

						print 'seg %d: %d -> %d ::: %3d' % (num_segments, data_offset, offset, offset - data_offset)
						num_segments += 1
					else:
						print 'DAMN!!!!!!!!!!!!!'
				print ''

			for i in xrange(len(self.entries)):
				entry = self.entries[i]

				entries_list_file.write('0x%08x\n' % entry.hash)
				
				self.file.seek(entry.offset)
				magic = unpack(self.endianness + 'I', self.file.read(calcsize(self.endianness + 'I')))[0]
				self.file.seek(-calcsize(self.endianness + 'I'), os.SEEK_CUR)
				if magic == unpack_from('>I', 'segs')[0]:
					print 'processing multi...'
					print '\tHash: 0x%08x' % entry.hash
					print '\tOffset: %d' % entry.offset
					print '\tSize1: %d' % entry.size1
					print '\tSize2: %d' % entry.size2
					print '\tSize3: %d' % entry.size3
					self.processMulti(entry)
				else:
					print 'processing single...'
					print '\tHash: 0x%08x' % entry.hash
					print '\tOffset: %d' % entry.offset
					print '\tSize1: %d' % entry.size1
					print '\tSize2: %d' % entry.size2
					print '\tSize3: %d' % entry.size3
					self.processSingle(entry)
				print ''

def processFile(file_name):
	endianness = None
	if file_name.endswith('.pc'):
		endianness = '<'
	elif file_name.endswith('.ps3'):
		endianness = '>'
	elif file_name.endswith('.360'):
		print 'Xbox 360 format is not supported for now'
		return
	else:
		print 'Unknown format'
		return

	with open(file_name, 'rb') as file:
		try:
			arc = BigArchive(file, endianness)
			arc.unpack()
		except EOFError:
			print 'Failed open file'
			return

mkdirSafe('entries')
mkdirSafe('segments')

map(lambda x: processFile(x) if os.path.exists(x) else None, sys.argv[1:])
