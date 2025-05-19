# Talk

- [Talk](#talk)
  - [Challenge Description](#challenge-description)
  - [General Idea](#general-idea)
  - [Socket Communication sequence](#socket-communication-sequence)
  - [Solution](#solution)

## Challenge Description

We managed to sniff some traffic from a TLS connection. The pcap traffic is encrypted, but set up keylog and have the private key of the server. Can you help us decrypt it to find out what the server is sending to the client? We also managed to obtain some other files which may render helpful.

File [talk.zip](../challenge/talk.zip) consists of:
- [logs/traffic.pcap](../challenge/logs/traffic.pcap)
- [logs/ssl_keylog](../challenge/logs/ssl_keylog)
- [certs/self-signed.crt](../challenge/certs/self-signed.crt)
- [certs/self-signed.key](../challenge/certs/self-signed.key)
- [crypto.py](../challenge/crypto.py)

## General Idea

- PCAP with provided keylog and private key is provided.
- Traffic consists of many TLS connections, some of which are important.
- The goal is to extract another Diffie-Hellman key exchange from the PCAP and try to break the AES cipher using the shared key.
- The aes key is derived using HKDF from the shared key

## Socket Communication sequence

Each time json is sent over TLS (can derive from the first shared key via HKDF) and is encrypted using AES.

| seq | client                       | server                        |
| --- | ---------------------------- | ----------------------------- |
| 1   | send hello                   |                               |
| 2   |                              | send g and p                  |
| 3   | send client public key A     |                               |
| 4   |                              | send server public key B      |
| 5   | send first packet (aes encr) |                               |
| 6   |                              | send second packet (aes encr) |
| 7   | send third packet (aes encr) |                               |
| 8   |                              | send fourth packet (aes encr) |

## Solution

Let's use the provided keylog file to decrypt the TLS traffic in the pcap file.
You can use wireshark to search through packets interactively, or dump everything at once using the following `tshark` command:

```bash
#!/bin/bash

tshark -r ./logs/traffic.pcap -V -x -q \
    -o "tls.debug_file:ssldebug.log" \
    -o "tls.desegment_ssl_records: TRUE" \
    -o "tls.desegment_ssl_application_data: TRUE" \
    -o "tls.keys_list:certs/self-signed.key" \
    -o "tls.keylog_file:./logs/ssl_keylog" \
    -Y "http"
```

Let's now analyze the traffic to see that at some point the decrypted information becomes useful.

```bash
Plaintext[174]:
| 7b 22 73 74 61 74 75 73 22 3a 20 22 6b 65 78 22 |{"status": "kex"|
| 2c 20 22 71 77 65 69 6f 72 76 75 77 65 68 72 76 |, "qweiorvuwehrv|
| 6f 69 22 3a 20 31 31 2c 20 22 70 66 38 69 6a 33 |oi": 11, "pf8ij3|
| 34 70 66 6f 33 38 22 3a 20 39 35 35 39 30 33 36 |4pfo38": 9559036|
| 31 36 30 35 31 34 32 36 34 30 30 30 39 30 38 30 |1605142640009080|
| 37 38 39 31 32 36 33 34 33 34 33 38 35 39 35 35 |7891263434385955|
| 39 34 37 34 38 35 33 33 35 34 35 36 38 31 31 34 |9474853354568114|
| 36 32 30 30 32 32 38 37 34 32 35 32 33 30 39 33 |6200228742523093|
| 33 35 37 30 30 36 31 33 32 37 34 34 32 30 33 32 |3570061327442032|
| 32 39 36 34 32 34 33 30 35 35 34 32 38 37 39 37 |2964243055428797|
| 39 32 30 33 33 30 32 38 31 30 32 37 7d 17       |920330281027}.  |
tls_save_decrypted_record found 0 padding bytes
ssl_add_record_info stored decrypted record seq=0 nxtseq=173 flow=0x65087601cdc0
dissect_ssl_payload decrypted len 173
decrypted app data fragment[173]:
| 7b 22 73 74 61 74 75 73 22 3a 20 22 6b 65 78 22 |{"status": "kex"|
| 2c 20 22 71 77 65 69 6f 72 76 75 77 65 68 72 76 |, "qweiorvuwehrv|
| 6f 69 22 3a 20 31 31 2c 20 22 70 66 38 69 6a 33 |oi": 11, "pf8ij3|
| 34 70 66 6f 33 38 22 3a 20 39 35 35 39 30 33 36 |4pfo38": 9559036|
| 31 36 30 35 31 34 32 36 34 30 30 30 39 30 38 30 |1605142640009080|
| 37 38 39 31 32 36 33 34 33 34 33 38 35 39 35 35 |7891263434385955|
| 39 34 37 34 38 35 33 33 35 34 35 36 38 31 31 34 |9474853354568114|
| 36 32 30 30 32 32 38 37 34 32 35 32 33 30 39 33 |6200228742523093|
| 33 35 37 30 30 36 31 33 32 37 34 34 32 30 33 32 |3570061327442032|
| 32 39 36 34 32 34 33 30 35 35 34 32 38 37 39 37 |2964243055428797|
| 39 32 30 33 33 30 32 38 31 30 32 37 7d          |920330281027}   |
```

We identified the important conversation in the decrypted traffic. These `kex` parameters suggest it is a known key exchange schema.
Let's extract the Diffie-Hellman key exchange from the important conversation.

```py
import re
from crypto import derive_key, decrypt_json, decode_json, long2bytes

log_data = open('ssldebug.log').read()

# It's just a parser function for the tshark output
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
g, p, A, B, key = 0, 0, 0, 0, 0

# We start analyzing from the 162nd packet, because no packet before is useful, they are just random hello-s sent one way.
o = 162

for i, fragment in enumerate(decrypted_fragments, start=1):
    if i == o+1:
        print(f"Fragment {i} skip")
    elif i == o+2:
        # having read two big numbers, and "pub" parameters (public keys) we can deduce it is a key exchange
        print(f"Fragment {i} p,g")
        fragment = decode_json(bytes.fromhex(fragment))

        # simple relabeling of g, and p. They are easily distinguishable from one another provided their length.
        g = int(fragment.get("qweiorvuwehrvoi"))
        p = int(fragment.get("pf8ij34pfo38"))
        print(f"g={g}")
        print(f"p={p}")
    elif i == o+3:
        # now we fetch the public key of A, which in Diffie-Hellman is calculated using A=a^g mod p, where a is the private key
        fragment = decode_json(bytes.fromhex(fragment))
        A = int(fragment.get("pub"))
        print(f"Fragment {i} A={A}")
    elif i == o+4:
        # now we fetch the public key of B, B=b^g mod p, where b is the private key 
        fragment = decode_json(bytes.fromhex(fragment))
        B = int(fragment.get("pub"))
        print(f"Fragment {i} B={B}")
        # We know we are provided with both public keys. The numbers are not *very* large, therefore we can calculate the DLP.
        # Here I chose to crack a
        print(f"Use cracking software like https://www.alpertron.com.ar/DILOG.HTM")
        a = input("Cracked private key a:") # challenge files can be solved with a = 187 372921 205030 131751 878949 770025 405551 886275 022280 716599
        a = int(a.replace(" ", ""))
        # Shared key can be written as B^a mod p or A^b mod p
        key = pow(B, a, p)
        print(f"Fragment {i} Shared key: {key}")
    elif i == o+5:
        # We are now using two functions from crypto.py which was provided in the challenge files
        # We know shared key is an integer. 
        # Function signatures:
        # - long2bytes has int -> bytes, 
        # - derive_key has bytes -> bytes
        # long2bytes . derive_key (key) :: int -> bytes, everything works as encrypt_json :: (bytes -> dict) -> bytes also takes bytes
        key = derive_key(long2bytes(key))
        fragment = decrypt_json(key, bytes.fromhex(fragment))
        print(f"Fragment {i} - login and password: {fragment}")
    elif i == o+6:
        # The hardest part here is to understand, that derive key can be used to create a single ratchet.
        # It is a standard for various e2e encryption schemas
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
```

Running the scripts:

```bash
./tshark.sh
python solve.py
Fragment 163 skip
Fragment 164 p,g
g=11
p=9559036160514264000908078912634343859559474853354568114620022874252309335700613274420322964243055428797920330281027
Fragment 165 A=6941423384766158224392025156909189920470651960178771771904097599946522567682156710320107540933450296470325751063928
Fragment 166 B=8409012044384318258907152702296430839745841035059732266832533711752917010999352129399593271390511892928105631845602
Use cracking software like https://www.alpertron.com.ar/DILOG.HTM
Cracked private key a:187 372921 205030 131751 878949 770025 405551 886275 022280 716599 
Fragment 166 Shared key: 7980800657788537152790132490675396347903012317037054540573797596953201375679993213690229553415037282324020732754165
Fragment 167 - login and password: {'login': 'admin', 'password': 'admin1293rf980234fh32890f72g3h4rf908327h34928c7h34f98237yhf3987g987ghggg'}
Fragment 168 - token: {'status': 'ok', 'token': '463031f309fc1ff62e3d0f7d14f92c8399a4f3ad8bb6c57f84b64d5bceb51c7768a3794a3df8eb9efc8e9c9107369f127193b442cb1ac809f25decf8c5a29c48'}
Fragment 169 - profile: {'profile': 'me'}
Fragment 170 - profile data (FLAG): {'data': 'BtSCTF{cf75_SIMPLE_c_KEY_47e0937f8b7acc_EXCHANGE_e7bbc1c0707280dd4cee7}'}
```

We obtain the flag:

```
BtSCTF{cf75_SIMPLE_c_KEY_47e0937f8b7acc_EXCHANGE_e7bbc1c0707280dd4cee7}
```