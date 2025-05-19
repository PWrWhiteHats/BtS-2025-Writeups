# Better AES

## Code examination
The challenge provides an encrypted flag and a possibility to encrypt your own block.
The new encryption key is generated every time the challenge program is run.

We see that S-box was changed to identity transformation, so it doesn't make anything:
```python
# for easier testing
sbox = list(range(0, 256))
```

The backend doesn't allow to encrypt block consisting of only zeros:
```python
if block == b'\0' * 16:
    raise Exception('Wanna encrypt null? What a terrible waste of resources!')
```

## Vulnerability
The main vulerability is the de facto lack of substitution step, since s-box is identity function,
which makes the whole cipher an affine transformation
(a linear transformation plus a constant derived from encryption key):
```
y = L(x) + C = Mx + C
```
Where x is an input binary vector, y an output binary vector, L(x) a linear transformation M the transformation matrix, C the constant.
All we need to decrypt the flag is to know that transformation with its inverse and a constant.

## Solution
To get a linear transformation and its inverse, we can modify encrypt_block and decrypt_block functions
in a way they don't perform key XOR-ing:
```python
def linear_transform(self, plaintext):
    state = list(plaintext)
    for rnd in range(1, self.NUM_ROUNDS):
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.mix_columns(state)
    state = self.sub_bytes(state)
    state = self.shift_rows(state)
    return bytes(state)

def inverse_linear_transform(self, ciphertext):
    state = list(ciphertext)
    for rnd in range(self.NUM_ROUNDS - 1, 0, -1):
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.inv_mix_columns(state)
    state = self.inv_shift_rows(state)
    state = self.inv_sub_bytes(state)
    return bytes(state)
```

The obvious way to get the constant is to encrypt a null vector, which leads to:
```
y = M*O + C = C 
```
but encrypting a null vector is not allowed, so we need another way.

We can also take any vector we know and transform unencrypted vector locally:
``` 
y' = L(x')
```
So we know a transformed vector `L(x')`
And encrypt the same vector `x'` at the remote service:
```
y'' = L(x') + C
```

Since we know both the encrypted vector `y''` and transformed one `L(x)`, we can get the constant:
```
C = y'' - L(x')
```
Since these all are binary vectors, subtraction is the same as addition (both are just XORing)

When we have both inverse transformation and the constant, we can recover the flag block by block:
``` 
flag_block = L^(-1)(encrypted_flag_block XOR C)
```

```python
def recover_flag(self, ciphertext: bytes, affine_const: bytes):
    output = b''
    for i in range(0, len(ciphertext), self.BLOCK_SIZE):
        block = ciphertext[i:i + self.BLOCK_SIZE]
        transformed_flag_part = bytes(x1 ^ x2 for x1, x2 in zip(block, affine_const))
        output += self.inverse_linear_transform(transformed_flag_part)
    return output
```

Since the flag is padded with zeros to the full block length, we can the leading zeros off and we have it.

### Full solution code
```python
from better_aes import BetterAES
from pwn import *

TARGET_HOST = '127.0.0.1'
TARGET_PORT = 13377


class BetterCracker(BetterAES):
    def __init__(self):
        super(BetterCracker, self).__init__(bytes(32))

    # modified decrypt without key adding
    def linear_transform(self, plaintext):
        state = list(plaintext)
        for rnd in range(1, self.NUM_ROUNDS):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        return bytes(state)

    # modified decrypt
    def inverse_linear_transform(self, ciphertext):
        state = list(ciphertext)
        for rnd in range(self.NUM_ROUNDS - 1, 0, -1):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.inv_mix_columns(state)
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        return bytes(state)

    def recover_flag(self, ciphertext: bytes, affine_const: bytes):
        output = b''
        for i in range(0, len(ciphertext), self.BLOCK_SIZE):
            block = ciphertext[i:i + self.BLOCK_SIZE]
            transformed_flag_part = bytes(x1 ^ x2 for x1, x2 in zip(block, affine_const))
            output += self.inverse_linear_transform(transformed_flag_part)
        return output


def main():
    cracker = BetterCracker()

    # could be anything, 1 bit is easy to illustrate
    to_encrypt = b'\0' * 15 + b'\x01'
    transformed_one = cracker.linear_transform(to_encrypt)
    print(f'Transformed one: {transformed_one.hex()}')

    conn = remote(TARGET_HOST, TARGET_PORT)
    encrypted_flag_part = conn.recvuntil(
        b'Enter something you want to encrypt in hex form: ').decode()
    flag_ciphertext = bytes.fromhex(encrypted_flag_part.split()[2])
    print('Flag ciphertext:', flag_ciphertext)

    conn.send(to_encrypt.hex().encode() + b'\n')
    encrypted_user_input_part = conn.recvuntil(b'Goodbye').decode()
    encrypted_one = bytes.fromhex(encrypted_user_input_part.split(':')[1].split()[0])

    affine_constant = bytes(x1 ^ x2 for x1, x2 in zip(transformed_one, encrypted_one))

    recovered_flag = cracker.recover_flag(flag_ciphertext, affine_constant)

    print(recovered_flag.decode().replace('\0', ''))


if __name__ == '__main__':
    main()

```
