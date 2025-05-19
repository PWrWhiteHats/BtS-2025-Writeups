import json
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Decode json from bytes
def decode_json(data: bytes) -> dict:
    try:
        return json.loads(data.decode())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON: {e}")
    
# Encode json to bytes
def encode_json(data: dict) -> bytes:
    try:
        return json.dumps(data).encode()
    except (TypeError, ValueError) as e:
        raise ValueError(f"Failed to encode JSON: {e}")

# Initial Key Manipulation
def long2bytes(n: int) -> bytes:
    """Convert a long integer to bytes."""
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, 'big')

# Key Derivation using HKDF
def derive_key(shared_bytes: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
    )
    return hkdf.derive(shared_bytes)

# AES ECB Encryption
def encrypt_json(key: bytes, data: dict) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    plaintext = json.dumps(data).encode()
    padding_length = 16 - len(plaintext) % 16
    plaintext += bytes([padding_length]) * padding_length
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

# AES ECB Decryption
def decrypt_json(key: bytes, data: bytes) -> dict:
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(data) + decryptor.finalize()
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    return json.loads(plaintext)