from secrets import token_bytes

class BetterAES:
    BLOCK_SIZE = 16          # Block size in bytes
    KEY_SIZE = 32            # Key size in bytes (256 bits)
    NUM_ROUNDS = 14          # Number of rounds for AES-256

    # Round constants
    RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    # for easier testing
    sbox = list(range(0, 256))

    def __init__(self, key: bytes):
        self.aes_256_key = key

        # inverse S-box
        self.inv_sbox = [0] * 256
        for i, v in enumerate(self.sbox):
            self.inv_sbox[v] = i

    def gf_mult(self, a, b):
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            high = a & 0x80
            a = (a << 1) & 0xFF
            if high:
                a ^= 0x1B
            b >>= 1
        return result

    def sub_bytes(self, state):
        return [self.sbox[b] for b in state]

    def inv_sub_bytes(self, state):
        return [self.inv_sbox[b] for b in state]

    def shift_rows(self, state):
        new = [0] * 16
        for r in range(4):
            for c in range(4):
                new[r + 4*c] = state[r + 4*((c + r) % 4)]
        return new

    def inv_shift_rows(self, state):
        new = [0] * 16
        for r in range(4):
            for c in range(4):
                new[r + 4*c] = state[r + 4*((c - r) % 4)]
        return new

    def mix_columns(self, state):
        new = state.copy()
        for c in range(4):
            col = state[4*c:4*c+4]
            new[4*c + 0] = self.gf_mult(col[0], 2) ^ self.gf_mult(col[1], 3) ^ col[2] ^ col[3]
            new[4*c + 1] = col[0] ^ self.gf_mult(col[1], 2) ^ self.gf_mult(col[2], 3) ^ col[3]
            new[4*c + 2] = col[0] ^ col[1] ^ self.gf_mult(col[2], 2) ^ self.gf_mult(col[3], 3)
            new[4*c + 3] = self.gf_mult(col[0], 3) ^ col[1] ^ col[2] ^ self.gf_mult(col[3], 2)
        return new

    def inv_mix_columns(self, state):
        new = state.copy()
        for c in range(4):
            col = state[4*c:4*c+4]
            new[4*c + 0] = self.gf_mult(col[0], 0x0e) ^ self.gf_mult(col[1], 0x0b) ^ self.gf_mult(col[2], 0x0d) ^ self.gf_mult(col[3], 0x09)
            new[4*c + 1] = self.gf_mult(col[0], 0x09) ^ self.gf_mult(col[1], 0x0e) ^ self.gf_mult(col[2], 0x0b) ^ self.gf_mult(col[3], 0x0d)
            new[4*c + 2] = self.gf_mult(col[0], 0x0d) ^ self.gf_mult(col[1], 0x09) ^ self.gf_mult(col[2], 0x0e) ^ self.gf_mult(col[3], 0x0b)
            new[4*c + 3] = self.gf_mult(col[0], 0x0b) ^ self.gf_mult(col[1], 0x0d) ^ self.gf_mult(col[2], 0x09) ^ self.gf_mult(col[3], 0x0e)
        return new

    def add_round_key(self, state, key):
        return [b ^ k for b,k in zip(state,key)]

    def key_expansion(self, key):
        if len(key) != self.KEY_SIZE:
            raise ValueError("Key must be 32 bytes")
        expanded = list(key)
        i = self.KEY_SIZE
        rcon_i = 0
        while len(expanded) < self.BLOCK_SIZE * (self.NUM_ROUNDS + 1):
            temp = expanded[-4:]
            if i % self.KEY_SIZE == 0:
                # RotWord + SubWord + Rcon
                temp = temp[1:] + temp[:1]
                temp = [self.sbox[b] for b in temp]
                temp[0] ^= self.RCON[rcon_i]
                rcon_i += 1
            elif i % self.KEY_SIZE == 16:
                # SubWord only
                temp = [self.sbox[b] for b in temp]
            for j in range(4):
                expanded.append(expanded[i - self.KEY_SIZE + j] ^ temp[j])
            i += 4
        # split into round keys
        return [expanded[16*r:16*(r+1)] for r in range(self.NUM_ROUNDS+1)]

    def encrypt_block(self, plaintext):
        key = self.aes_256_key
        if len(plaintext) != self.BLOCK_SIZE or len(key) != self.KEY_SIZE:
            raise ValueError("Plaintext must be 16 bytes and key 32 bytes")
        state = list(plaintext)
        round_keys = self.key_expansion(key)
        state = self.add_round_key(state, round_keys[0])
        for rnd in range(1, self.NUM_ROUNDS):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, round_keys[rnd])
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, round_keys[self.NUM_ROUNDS])
        return bytes(state)

    def decrypt_block(self, ciphertext):
        key = self.aes_256_key
        if len(ciphertext) != self.BLOCK_SIZE or len(key) != self.KEY_SIZE:
            raise ValueError("Ciphertext must be 16 bytes and key 32 bytes")
        state = list(ciphertext)
        round_keys = self.key_expansion(key)
        state = self.add_round_key(state, round_keys[self.NUM_ROUNDS])
        for rnd in range(self.NUM_ROUNDS-1, 0, -1):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, round_keys[rnd])
            state = self.inv_mix_columns(state)
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, round_keys[0])
        return bytes(state)

    def encrypt(self, plaintext: bytes):
        # split to blocks
        blocks = []
        for i in range(0, len(plaintext), self.BLOCK_SIZE):
            blocks.append(plaintext[i:i + self.BLOCK_SIZE])
        # pad
        if blocks:
            blocks[-1] = blocks[-1] + b'\0' * (self.BLOCK_SIZE - len(blocks[-1]))
        # encrypt with ECB
        output = b''
        for block in blocks:
            if block == b'\0' * 16:
                raise Exception('Wanna encrypt null? What a terrible waste of resources!')
            output += self.encrypt_block(block)
        return output


def main():
    with open('flag', 'rb') as f:
        flag = f.read().strip()
    key = token_bytes(32)

    aes_crypt = BetterAES(key)
    ct = aes_crypt.encrypt(flag)
    print(f"Flag ciphertext: {ct.hex()}")

    try:
        print("Enter something you want to encrypt in hex form: ", end="")
        input_hex = input()

        if input_hex:
            if len(input_hex) <= 32:
                user_input = bytes.fromhex(input_hex)
                encrypted = aes_crypt.encrypt(user_input)
                print(f'Encrypted: {encrypted.hex()}')
            else:
                print('Input too long')
        else:
            print('Enter valid hex string')
    except ValueError:
        print('Invalid hex string')
    except Exception as e:
        print(e)
    print('Goodbye')


if __name__ == '__main__':
    main()
