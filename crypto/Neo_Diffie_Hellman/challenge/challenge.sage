from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random
from Crypto.Util.Padding import pad


p = 1000117

Fq = GF(p)

G = matrix(Fq, [[8544, 7125, 942, 1054, 2338, 8223, 1149, 3981],
                [7803, 9243, 6830, 8788, 9576, 1916, 7762, 5861],
                [9026, 9381, 9235, 994, 6194, 508, 7351, 1406],
                [6410, 6445, 6086, 653, 1783, 4564, 8874, 4739],
                [2797, 8921, 113, 1078, 6810, 7392, 3659, 1316],
                [1688, 1010, 631, 6495, 7379, 5804, 7237, 527],
                [2211, 4452, 1519, 498, 9284, 3282, 9628, 4355],
                [1267, 9413, 3340, 2316, 8627, 1310, 4481, 4808]])

secret_a = random.randint(int(1000000), int(100000000))
secret_b = random.randint(int(1000000), int(100000000))

pub_a = G^secret_a
pub_b = G^secret_b

print("pubkey A:")
print(pub_a)
print("pubkey B:")
print(pub_b)

key_a = pub_b^secret_a
key_b = pub_a^secret_b

assert key_a == key_b

flattened = key_a.list()
matrix_bytes = ",".join(map(str, flattened)).encode('utf-8')

key = sha256(matrix_bytes).digest()

flag = open('flag', 'r').read().encode()

iv = get_random_bytes(16)
padded_plaintext = pad(flag, AES.block_size)

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(padded_plaintext)

print(f"iv: {iv.hex()}")
print(f"flag: {ciphertext.hex()}")