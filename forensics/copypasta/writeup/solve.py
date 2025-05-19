from PyPDF2 import _encryption
from Crypto.Cipher import AES
from hashlib import md5
import binascii
import zlib
import re
from data import cmap, text_object

P = -3392 & 0xFFFFFFFF

O = bytes([
    0x4D, 0x47, 0x2C, 0xBB, 0x7F, 0xB4, 0x22, 0x99, 0xFA, 0x91, 0xD5, 0x57, 0xDC, 0x4D, 0xE7, 0x81, 
    0x86, 0x87, 0x67, 0xDC, 0x39, 0xB1, 0xE8, 0x78, 0x92, 0x86, 0xEE, 0x34, 0x32, 0x82, 0xD5, 0xA2, 
])

ID1 = bytes([
    0xD3, 0x11, 0x71, 0x96, 0xA8, 0xBC, 0xB2, 0x11,
    0x0A, 0x00, 0x67, 0x45, 0x8B, 0x6B, 0xC6, 0x23
])

def load_passwords(path: str) -> list[bytes]:
        with open(path, "r") as f:
            return list(map(lambda x: x.strip().encode(), f.readlines()))

def decrypt_and_inflate_object(enc_key: bytes, obj_id: int, obj_data: bytes) -> bytes:
    obj_salt = bytes([obj_id, 0x00, 0x00, 0x00, 0x00, 0x73, 0x41, 0x6c, 0x54])
    final_enc_key = md5(enc_key + obj_salt).digest()
    iv = obj_data[:16]
    cipher = AES.new(final_enc_key, AES.MODE_CBC, iv)
    deflated = cipher.decrypt(obj_data[16:])
    return zlib.decompress(deflated)

def find_enc_key(passwords: list[bytes], o: bytes, p: int, id1: bytes, test_obj_id: int, test_obj_data: bytes):
    for pw in passwords:
        test_enc_key = _encryption.AlgV4.compute_key(
            rev=4, 
            key_size=128, 
            password=pw, 
            o_entry=o, 
            id1_entry=id1, 
            P=p, 
            metadata_encrypted=True
        )
        
        try:
            decrypt_and_inflate_object(test_enc_key, test_obj_id, test_obj_data)
            return test_enc_key
        except:
            pass
        

def main():
    passwords = load_passwords(path="./wordlist.txt")
    enc_key = find_enc_key(passwords, O, P, ID1, 42, cmap)
    cmap_decoded = decrypt_and_inflate_object(enc_key, 42, cmap).decode()
    text_object_decoded = decrypt_and_inflate_object(enc_key, 43, text_object).decode()
    unicode_map  = [int(x, 16) for _, x in re.findall(r'<(\S+?)>\s*<(\S+?)>', cmap_decoded)]
    keycodes = binascii.unhexlify(''.join(re.findall(r'<([0-9A-Fa-f]+)>', text_object_decoded)))
    print(''.join([chr(unicode_map[x]) for x in keycodes]))

if __name__ == "__main__":
    main()