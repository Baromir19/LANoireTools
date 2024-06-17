# Main
These tools were created to modify L.A.Noire.

The tools for "oldscripts" were created by other people, I only found them in the archives of the Internet:
* `010 Tools` was created by Kramla
* `Python2 .big unpacker` was created by flatz
* `BMS .big unpacker` was created by Falo (not sure)
* `010 Tools` for Nintendo Switch ver. can be found [here](https://github.com/masagrator/LANoireNX)
* `.fsb4 unpacker` can be found [here](https://hcs64.com/vgm_ripping.html) (fsb_mpeg). For packaging, you need to make a WAV format from MP3, and then convert it using [fsbankex.exe](https://www.playground.ru/mafia_2/file/mafia_2_konvertatsiya_muzyki_k_igre-888201?ysclid=lwhv6vorvu171450274)
* `Havok data` export can be found [here](https://lukascone.wordpress.com/2024/03/12/havok-middleware/). More about havok header (sometimes included in ptM#) is [here](https://zeldamods.org/w_botw/index.php?title=Havok&mobileaction=toggle_view_desktop)
* `BMFont` is the format that was used to create the in-game fonts, the program to generate [here](https://www.angelcode.com/products/bmfont/)

New scripts were created by me (unpacker of big files based on Python2 big unpacker):
* `bigpc3_unpack.py` - unpacks the .big.pc archive, uses Python 3. The file has entries, each entry is divided into chunks, which are 128 kilobytes in size when unpacked (except for the last chunk, which can be any size up to 128 kilobytes, which is necessary to pack the entry). Chunks are packed in "deflate" format (RFC1950/1/2, untitled, unmagisked);
* `bigpc3_pack.py` - performs packing of the catalog into big.pc. The packaging result does not match the original archive (probably in the original archiving a slightly modified zlib (deflate 1.2.3) was used, or special settings for deflate). **It is advisable to make a backup of the original!** The packaging was checked (when unpacking, all files matched the original ones by hash), the packaged archive was used instead of the original one for launch L.A.Noire, no problems identified. I still didn't understand the logic of the segments that were compressed without the segment table (case 0);
* `wad_unpack.py` - unpacks the .wad archive. Probably (I'm not sure) the archive is outdated and not used in the final version. But it has a lot of original files, which will be useful for further unpacking of files. I have no plans to write a packer, although writing it will not be a problem (you just need to save the crc32 values, or get them);
* `trunk_unpack.py` - unpacks the .trunk archive (has a trM# header, use the fileext.py script). As far as I understand, this extension stores 3D models or just textures (for example, in DLC5 there was an image of a phelps suit for the costume selection menu). Includes unknown file formats, probably some of which are metadata;
* `atb_to_xml.py` - unpacks .atb into an .xml file. It was created at the request of LANoire. It is not clear whether LANoire can read .xml files instead of .atb chunks, especially since there are many problems that I have not solved (the format of the names of the .xml files, the root tag, as well as the names of objects and their type);
* `xml_to_atb.py` - packs .xml into an .atb file. Hash sum of the repacked and original ATB files match
* `dictionaries.py` - additional file for atb_to_xml, includes the types and sizes of variables behind the byte, as well as the types of objects behind the signature;
* `fileext.py` - adds a file extension (dictionary-based). The script is intended to understand and work with file types, not to use them later (for which you need to get a full name from hash, which is described in Section 3). In order to add an extension, the 2nd parameter must be True, to remove the extension - False;
* `atb_unpack.py`/`atb_directory_unpack.py` - unpacks strings from the .atb file(-s) (deprecated, but may be useful to someone);
* `atb_to_array.py` - performs a complete decompression of the archive into arrays, which in the future can be processed at your own request.

## How to use
* `atb_to_xml.py` - expects a string with the file name. If the file was not specified as an argument, then it should be entered manually after startup. If the file is not found, the program raises an exception;
* `bigpc3.py` - expects a string with the path to .big file.

## Useful information
Theoretically, you don't need to pack the files, you just need to know their full converted names. According to Falo, these names can be found in the .atb files, but there are real names indicated there, they need to be converted to L.A.Noire format (atb -> chunk.atb, dae -> chunk). The converted file format can be found using a hash function (the function was also found by Falo, I placed it in `additional_functions.py`). An example induced by Falo:
- real filename: characters/dead_bodies/pt007_kenneth_temple.dae
- converted filename: intermediate/chunks/characters/dead_bodies/pt007_kenneth_temple.chunk

.atb files has next format: `intermediate/chunks/attribute/root."BIGNAME"."ATBNAME".atb.chunk`, where "BIGNAME" is name of .big file (no file format, f.e. "dlc.dlc4"), "ATBNAME" - name of .atb file (with my .atb to .xml tool you can see that among the upper classes or collections there is a file name in a format of 2 letters and 3 numbers, f.e. "at004". Is optional in the name).

The ptM# file is probably an archive that includes .dae, .sdk, ragdoll, animations, texture pointers (for example, 0x5669FF3C is the CRC for `textures/uistreamed_dlc/outfits/dlc05.tga`, it is specified in the DLC file for the texture of the selected outfit. In the game, however, this CRC is converted into a pointer to an abstract texture / shader).

Known extensions of the original files (extensions that are not likely to have been compressed are marked with *): 
* `.avi` - video extension?*
* `.ogv` - video extension (codec: Theora Movies). As far as I understand, it is packed in DGAD.
* `.bik` - video extension.
* `.mp3` - audio extension, compressed in FSB4, and also has a format without a header.
* `.tga` - it's the texture format. Probably either reformatted to .dds without transparency support, or packed in the DGAD archive.
* `.ico` - icons image were probably used in the development.
* `.fnt` - font extension. The game uses this extension, not .dds.
* `.sdk` - set driven keys extension.
* `.anim` - animation extension.
* `.vbs` - visual basic script, probably was used when building some files.*
* `.lua` - script file.
* `.txt` - text file, was used for logs.*
* `.png` - image format. In the game, it is packaged as dds, it is enough to use online converters.
* `.dae` - dagital asset extension format. As far as I understand, it is serialized in ptM#

You can get a hash (crc) from a string (object type/variable name) for an atb file using the get_crc_from_string function in `additional_functions.py` (a random search for variable names will not lead to anything good due to collisions).
