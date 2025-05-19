Useful documentation: 
https://www.w3.org/TR/2003/REC-PNG-20031110/#5Chunk-layout

Writeup:
1. Thereupon, since we have only one file with an unknown extension (file tool identifies it only as "data"), let's open this file in hex editior (e.g. hexed.it)
2. Notice that the magic number is spurious and simultaneously similar to PNG signature -> change hex data "89 4A 50 47" to "89 50 4E 47"
3. After the signature comes a series of chunks. Each chunk starts with 4 bytes for the length of the chunk, 4 bytes for the type, then the chunk content itself (with the length which was declared earlier) and 4 bytes of a checksum. We ought to analyze should all chunks are appropriate
3.1 The name of IHDR chunk was changed to RHDR. Also, IHDR has always 0x0D length. -> change hex data "00 00 00 0A 52 48 44 52" to "00 00 00 0D 49 48 44 52"
3.2 The length of sRGB chunk was changed to 1A, although we can see there is only one byte of data (00). We can also count it by the information given in point 3, since sRGB chunk has 13 bytes and the length, name and CRC takes 12 bytes of it  -> change hex data "00 00 00 1A" to "00 00 00 01" 
3.3 The name of gAMA chunk was changed to MAMA. Also, CRC of this chunk is incorrect. We can compute it using e.g. crc32 library in python. Examplary python code can be find in scripts/CRC.py -> change hex data "4D 41 4D 41 00 00 B1 8F 0B BC 61 05" to "67 41 4D 41 00 00 B1 8F 0B FC 61 05"
4. After that, the image should be readable, and the flag is yours. You can track your progress using pngcheck tool.
   
\* A small error slipped into the task during the simplification process, and part of the IEND header (its checksum) ended up in the middle of the text, which breaks the visual appearance. But that's not a problem! By analyzing the document, we can see that its CRC32 is indeed missing, so we can easily calculate it (example code: scripts/CRC_IEND.py) and search for this sequence of characters in the text. By moving it to the correct place, we will get a clean, proper image along with the flag.
