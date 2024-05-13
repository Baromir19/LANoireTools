# Main
These tools were created to modify L.A.Noire. Currently, they can only get information (unpacking), but in the future I will try to pack the files to big.pc (.ps3, .360).

The tools for "oldscripts" were created by other people, I only found them in the archives of the Internet:
* `010 Tools` was created by
* `Python2 .big unpacker` was created by
* `BMS .big unpacker` was created by
* `010 Tools` for Nintendo Switch ver. can be found here [here](https://github.com/masagrator/LANoireNX)

New scripts were created by me (unpacker of big files based on Python2 big unpacker):
* `bigpc3.py` - unpacks the .big.pc archive, uses Python 3;
* `fileext.py` - adds a file extension, currently adds the name of a small number of file types;
* `atb_unpack.py`/`atb_directory_unpack.py` - unpacks strings from the .atb file(-s) (deprecated, but may be useful to someone);
* `atb_to_array.py` - performs a complete decompression of the archive into arrays, which in the future can be processed at your own request;
* `atb_to_xml.py` - unpacks .atb into an .xml file. It was created at the request of LANoire. It is not clear whether LANoire can read .xml files instead of .atb chunks, especially since there are many problems that I have not solved (the format of the names of the .xml files, the root tag, as well as the names of objects and their type);
* `dictionaries.py` - additional file for atb_to_xml, includes the types and sizes of variables behind the byte, as well as the types of objects behind the signature.

## How to use
* `atb_to_xml.py` - expects a string with the file name. If the file was not specified as an argument, then it should be entered manually after startup. If the file is not found, the program raises an exception.
