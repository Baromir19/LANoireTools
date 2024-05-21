# Main
These tools were created to modify L.A.Noire. Currently, they can only get information (unpacking), but in the future I will try to pack the files to big.pc (.ps3, .360).

The tools for "oldscripts" were created by other people, I only found them in the archives of the Internet:
* `010 Tools` was created by Kramla
* `Python2 .big unpacker` was created by flatz
* `BMS .big unpacker` was created by Falo (not sure)
* `010 Tools` for Nintendo Switch ver. can be found [here](https://github.com/masagrator/LANoireNX)
* `.fsb4 unpacker` can be found [here](https://hcs64.com/vgm_ripping.html)

New scripts were created by me (unpacker of big files based on Python2 big unpacker):
* `bigpc3.py` - unpacks the .big.pc archive, uses Python 3. The file has entries, each entry is divided into chunks, which are 128 kilobytes in size when unpacked (except for the last chunk, which can be any size up to 128 kilobytes, which is necessary to pack the entry). Chunks are packed in "deflate" format (RFC1950/1/2, untitled, unmagisked), my attempts to pack them back were unsuccessful (the result was a file size larger than it was originally packed);
* `fileext.py` - adds a file extension, currently adds the name of a small number of file types;
* `atb_unpack.py`/`atb_directory_unpack.py` - unpacks strings from the .atb file(-s) (deprecated, but may be useful to someone);
* `atb_to_array.py` - performs a complete decompression of the archive into arrays, which in the future can be processed at your own request;
* `atb_to_xml.py` - unpacks .atb into an .xml file. It was created at the request of LANoire. It is not clear whether LANoire can read .xml files instead of .atb chunks, especially since there are many problems that I have not solved (the format of the names of the .xml files, the root tag, as well as the names of objects and their type);
* `dictionaries.py` - additional file for atb_to_xml, includes the types and sizes of variables behind the byte, as well as the types of objects behind the signature.

## How to use
* `atb_to_xml.py` - expects a string with the file name. If the file was not specified as an argument, then it should be entered manually after startup. If the file is not found, the program raises an exception;
* `bigpc3.py` - expects a string with the path to .big file.

## Useful information
Theoretically, you don't need to pack the files, you just need to know their full converted names. According to Falo, these names can be found in the .atb files, but there are real names indicated there, they need to be converted to L.A.Noire format (atb -> chunk.atb, dae -> chunk). The converted file format can be found using a hash function (the function was also found by Falo, I placed it in `additional_functions.py`). An example induced by Falo:
- real filename: characters/dead_bodies/pt007_kenneth_temple.dae
- converted filename: intermediate/chunks/characters/dead_bodies/pt007_kenneth_temple.chunk

.atb files has next format: `intermediate/chunks/attribute/root."BIGNAME"."ATBNAME".atb.chunk`, where "BIGNAME" is name of .big file (no file format, f.e. "dlc.dlc4"), "ATBNAME" - name of .atb file (with my .atb to .xml tool you can see that among the upper classes or collections there is a file name in a format of 2 letters and 3 numbers, f.e. "at004". Is optional in the name).

## About archiving
At this moment, I have been trying to compress the file to its original state. Alas, these attempts were unsuccessful, their size turned out to be ~0.5% larger. I don't understand the archiving process, building tables, etc., but probably the original compression method was the 1.2.3 version of the deflate (as far as I understand, it was the zlib 1.2.3). I used the [zlib.h library](https://github.com/OSDVF/zlib-win-x64) with different strategies, compression ratios, and memory types, but it didn't work. The best success I've had was using [libdeflate](https://github.com/ebiggers/libdeflate), which has 12 levels of compression, and the archive was only 50-100 bytes larger than the original archived segment.

I still didn't understand the logic of the segments that were compressed without the segment table (case 0). The segments in case 1 have no compression. The segments in case 2 are compressed (if their flag is not 0x00), the chunk size is 128 kilobytes. Chunks can also be divided into segments if they are given chunks with a flag value less than theirs (e.g. 0x10 before, 0x11 after, which probably means that the segment header is in 0x10). In addition, it is likely that L.A.Noire has a read buffer of 2^16. If the size of the compressed chunk is greater than 2^16, this value should be subtracted from the chunk size as many times as the size is greater than 2^16, and the number of subtracted values should be recorded as a byte of the coefficient.

