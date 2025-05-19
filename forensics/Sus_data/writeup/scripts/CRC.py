import binascii

chunk_data = bytes.fromhex("67414D410000B18F")  #name of chunk ("gAMA") and its body
crc = binascii.crc32(chunk_data) & 0xFFFFFFFF 
print(hex(crc))  
