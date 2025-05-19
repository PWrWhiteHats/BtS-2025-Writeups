import re
from crypto import derive_key, decrypt_json, decode_json, long2bytes

log_data = open('ssldebug.log').read()


def extract_decrypted_fragments(log_data):
    start_pattern = re.compile(r'decrypted app data fragment\[\d+\]:')
    end_pattern = re.compile(r'process_ssl_payload')

    lines = log_data.splitlines()

    decrypted_fragments = []
    capture = False
    current_fragment = []

    for line in lines:
        if start_pattern.search(line):
            if capture:
                decrypted_fragments.append("".join(current_fragment))
                current_fragment = []
            capture = True

        if capture:
            hex_part = re.findall(r'\|([0-9a-fA-F\s]+)\s\|', line)
            if hex_part:
                current_fragment.append(hex_part[0].replace(' ', ''))

        if end_pattern.search(line) and capture:
            decrypted_fragments.append("".join(current_fragment))
            capture = False
            current_fragment = []

    return decrypted_fragments


decrypted_fragments = extract_decrypted_fragments(log_data)

# fragment 1 - hello
# fragment 2 - g and p
# fragment 3 - A
# fragment 4 - B
# fragment 5 - login and password
# fragment 6 - token
# fragment 7 - profile
# fragment 8 - profile data (FLAG)

g, p, A, B, key = 0, 0, 0, 0, 0
o = 162

for i, fragment in enumerate(decrypted_fragments, start=1):
    if i == o+1:
        print(f"Fragment {i} skip")
    elif i == o+2:
        print(f"Fragment {i} p,g")
        fragment = decode_json(bytes.fromhex(fragment))
        g = int(fragment.get("qweiorvuwehrvoi"))
        p = int(fragment.get("pf8ij34pfo38"))
        print(f"g={g}")
        print(f"p={p}")
    elif i == o+3:
        fragment = decode_json(bytes.fromhex(fragment))
        A = int(fragment.get("pub"))
        print(f"Fragment {i} A={A}")
    elif i == o+4:
        fragment = decode_json(bytes.fromhex(fragment))
        B = int(fragment.get("pub"))
        print(f"Fragment {i} B={B}")
        print(f"Use cracking software like https://www.alpertron.com.ar/DILOG.HTM")
        a = input("Cracked private key a:")
        a = int(a.replace(" ", ""))
        key = pow(B, a, p)
        print(f"Fragment {i} Shared key: {key}")
    elif i == o+5:
        key = derive_key(long2bytes(key))
        fragment = decrypt_json(key, bytes.fromhex(fragment))
        print(f"Fragment {i} - login and password: {fragment}")
    elif i == o+6:
        key = derive_key(key)
        fragment = decrypt_json(key, bytes.fromhex(fragment))
        print(f"Fragment {i} - token: {fragment}")
    elif i == o+7:
        key = derive_key(key)
        fragment = decrypt_json(key, bytes.fromhex(fragment))
        print(f"Fragment {i} - profile: {fragment}")
    elif i == o+8:
        key = derive_key(key)
        fragment = decrypt_json(key, bytes.fromhex(fragment))
        print(f"Fragment {i} - profile data (FLAG): {fragment}")
