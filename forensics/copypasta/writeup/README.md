## Copypasta

I was moving one of the most relatable copypastas to me to a pendrive, but I think something went wrong during copying and pasting (hehe) and I can't open the file. To make matters worse, I forgot the password, but it should be one of those in a wordlist. Can you help me recover my favourite copypasta?

## Writeup

File attached as the challenge is damaged - you can't open it in any PDF reader. The intended solution is to decrypt and analyse the objects manually, using the [PDF standard](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/PDF32000_2008.pdf) as a reference.

For this revision of the PDF standard, you need the following values to generate the encryption key:
- P (user permissions)
- O value
- First entry of ID dictionary (essentialy the unique ID of the file)

Once you have those values, you can try decrypting a chunk with every password until you succeed:
```py
def decrypt_and_inflate_object(enc_key: bytes, obj_id: int, obj_data: bytes) -> bytes:
    obj_salt = bytes([obj_id, 0x00, 0x00, 0x00, 0x00, 0x73, 0x41, 0x6c, 0x54])
    final_enc_key = md5(enc_key + obj_salt).digest()
    iv = obj_data[:16]
    cipher = AES.new(final_enc_key, AES.MODE_CBC, iv)
    deflated = cipher.decrypt(obj_data[16:])
    return zlib.decompress(deflated)

def find_enc_key(passwords: list[bytes], o: bytes, p: int, id1: bytes test_obj_id: int, test_obj_data: bytes):
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
```

(You also need object ID, it is a part of the salt that is added to the master encryption key, so every object has a different key)

After you recover the password and look through the objects, one contains the information text (the last one) and one contains the character map that maps each key code to its Unicode value. Then, all you have to do is convert all keycodes to Unicode, and you have the flag:
```py
cmap_decoded = decrypt_and_inflate_object(enc_key, 42, cmap).decode()
text_object_decoded = decrypt_and_inflate_object(enc_key, 43, text_object).decode()
unicode_map  = [int(x, 16) for _, x in re.findall(r'<(\S+?)>\s*<(\S+?)>', cmap_decoded)]
keycodes = binascii.unhexlify(''.join(re.findall(r'<([0-9A-Fa-f]+)>', text_object_decoded)))
print(''.join([chr(unicode_map[x]) for x in keycodes]))
```

Result:

```using linux in front of class matesteacher says “Ok students, now open photoshop”start furiously typing away at terminal to install WineErrors out the BtSCTF{we_have_to_censor_that_oneEveryone else has already started their classworkI start to sweatInstall GIMP”Umm...what the _and_another_one” a girl next to me asksI tell her its GIMP and can do everything that photoshop does and IT’S FREE!“Ok class, now use the shape to to draw a circle!” the teacher saysI _and_finally_that_one} break down and cry and run out of the classI get beat up in the parking lot after school```

Flag:
`BtSCTF{we_have_to_censor_that_one_and_another_one_and_finally_that_one}`

## Unintended solution
We tried multiple PDF recovery solutions, and nothing seemed to work. Well, it turns  out that there is a site that will happily repair the PDF once you have the correct password 🫠

https://www.freepdfconvert.com/repair-pdf