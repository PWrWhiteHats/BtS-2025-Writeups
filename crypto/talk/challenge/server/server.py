import ssl
import socket
import os
import sys
import json
import random
import string

from crypto import derive_key, encrypt_json, decrypt_json, long2bytes

p = int(os.getenv('DH_MODULUS'))
g = int(os.getenv('DH_GENERATOR'))
b = int(os.getenv('DH_PRIVKEY_SERVER'))
flag = os.getenv('DH_FLAG')
B = pow(g, b, p)

keylog_file = '/logs/ssl_keylog'
if os.path.exists(keylog_file):
    os.remove(keylog_file)

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.keylog_filename = keylog_file

context.load_cert_chain(certfile='/certs/self-signed.crt', keyfile='/certs/self-signed.key')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind(('', 8443))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        with context.wrap_socket(conn, server_side=True) as ssock:
            print("Connection from:", addr)
        
            # 1. server receives init message
            payload = ssock.recv(16384)
            payload = json.loads(payload.decode())
            
            if payload.get("message") == "exit":
                sys.exit(0)
            
            if payload.get("message") == "healthcheck":
                random_length = random.randint(100, 1000)
                random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=random_length))
                response = {"status": "ok", "padding": random_message}
                ssock.send(json.dumps(response).encode())
                print("R1. Healthcheck successful:", payload)
                continue
            
            print("R1. client payload:", payload)

            # 2. server sends unencrypted g and p
            response = {"status": "kex", "qweiorvuwehrvoi": g, "pf8ij34pfo38": p}
            ssock.send(json.dumps(response).encode())
            print(f"T2. sent g={g} and p={p} to client")

            # 3. server receives unencrypted public key A
            payload = ssock.recv(2048)
            payload = json.loads(payload.decode())
            print("R3. Client Payload:", payload)
            
            # 4. server sends unencrypted public key B
            response = {"pub": str(B)}
            ssock.send(json.dumps(response).encode())
            print(f"T4. sent B={B} to client")
            
            pub = int(payload.get("pub"))
            shared_key = pow(pub, b, p)

            print("[Shared AES Key]", shared_key)
            
            # 5. server receives encrypted login password
            key = derive_key(long2bytes(shared_key))
            enc_payload = ssock.recv(16834)
            payload = decrypt_json(key, enc_payload)
            print(f"R5. received encrypted login data", payload)

            key = derive_key(key)
            # 6. server sends encrypted login response
            # key = derive_key(key)
            response = {"status": "ok", "token": "463031f309fc1ff62e3d0f7d14f92c8399a4f3ad8bb6c57f84b64d5bceb51c7768a3794a3df8eb9efc8e9c9107369f127193b442cb1ac809f25decf8c5a29c48"}
            enc_response = encrypt_json(key, response)
            ssock.send(enc_response)
            print("T6. sent encrypted token to client")

            key = derive_key(key)
            # 7. server receives encrypted payload
            # key = derive_key(key)
            enc_payload = ssock.recv(2048)
            payload = decrypt_json(key, enc_payload)
            print("R7. received encrypted payload", payload)

            key = derive_key(key)
            # 8. server sends encrypted data
            # key = derive_key(key)
            response = {"data": flag}
            enc_response = encrypt_json(key, response)
            ssock.send(enc_response)
