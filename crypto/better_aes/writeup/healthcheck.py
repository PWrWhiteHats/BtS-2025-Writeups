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
    print('Flag ciphertext:', flag_ciphertext.hex())

    conn.send(to_encrypt.hex().encode() + b'\n')
    encrypted_user_input_part = conn.recvuntil(b'Goodbye').decode()
    encrypted_one = bytes.fromhex(encrypted_user_input_part.split(':')[1].split()[0])

    affine_constant = bytes(x1 ^ x2 for x1, x2 in zip(transformed_one, encrypted_one))

    recovered_flag = cracker.recover_flag(flag_ciphertext, affine_constant)

    print(recovered_flag.decode().replace('\0', ''))


if __name__ == '__main__':
    main()
