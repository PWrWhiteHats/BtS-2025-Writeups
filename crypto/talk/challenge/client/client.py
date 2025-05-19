import ssl
import socket
import os
import json
import random
import string

from crypto import derive_key, encrypt_json, decrypt_json, long2bytes

a = int(os.getenv('DH_PRIVKEY_CLIENT'))
A = 0

context = ssl.create_default_context()
context.load_verify_locations('/certs/self-signed.crt')

for i in range(81):
    with socket.create_connection(('server', 8443)) as sock:
        with context.wrap_socket(sock, server_hostname='server') as ssock:
            payload = {"message": "healthcheck"}
            ssock.send(json.dumps(payload).encode())
            print("T1. Sent healthcheck to server")

            response = ssock.recv(2048)
            response_data = json.loads(response.decode())
            if response_data.get("status") == "ok":
                print("R1. Healthcheck successful:", response_data)
            else:
                print("R1. Healthcheck failed:", response_data)

with socket.create_connection(('server', 8443)) as sock:
    with context.wrap_socket(sock, server_hostname='server') as ssock:
        # 1. client sends unencrypted hello
        random_length = random.randint(100, 1000)
        random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=random_length))
        payload = {"message": "hello", "padding": random_message}
        ssock.send(json.dumps(payload).encode())
        print("T1. Sent hello to server")

        # 2. client receives unencrypted g and p
        response = ssock.recv(2048)
        # Parse the received JSON response to extract g and p
        response_data = json.loads(response.decode())
        if response_data.get("status") == "kex":
            p = response_data.get("pf8ij34pfo38")
            g = response_data.get("qweiorvuwehrvoi")
            A = pow(g, a, p)
        else:
            raise ValueError("Unexpected response from server")
        print("R2. Received g and p from server:", g, p)

        # 3. client sends unencrypted public key A
        payload = {"pub": A}
        ssock.send(json.dumps(payload).encode())
        print(f"T3. Sent public key A to server {A}")

        # 4. client receives unencrypted public key B
        response = ssock.recv(2048)
        response_data = json.loads(response.decode())
        if response_data.get("pub") is not None:
            B = int(response_data.get("pub"))
        else:
            raise ValueError("Unexpected response from server")
        print("R4. Received public key B from server:", B)

        # create shared key
        shared_key = pow(B, a, p)
        print("Shared key:", shared_key)

        # 5. client sends encrypted credentials
        key = derive_key(long2bytes(shared_key))
        payload = {"login": "admin",
                   "password": "admin1293rf980234fh32890f72g3h4rf908327h34928c7h34f98237yhf3987g987ghggg"}
        enc_payload = encrypt_json(key, payload)
        ssock.send(enc_payload)
        print("T5. Sent encrypted credentials to server")

        key = derive_key(key)
        # 6. client receives encrypted token
        # key = derive_key(shared_key)
        enc_response = ssock.recv(2048)
        response = decrypt_json(key, enc_response)
        print("R6. Received encrypted token from server:", response)

        key = derive_key(key)
        # 7. client sends encrypted token
        # key = derive_key(shared_key)
        payload = {"profile": "me"}
        enc_payload = encrypt_json(key, payload)
        ssock.send(enc_payload)
        print("T7. Sent encrypted token to server")

        key = derive_key(key)
        # 8. client receives encrypted payload
        # key = derive_key(shared_key)
        enc_response = ssock.recv(2048)
        response = decrypt_json(key, enc_response)
        print("R8. Received encrypted payload from server:", response)

for i in range(43):
    with socket.create_connection(('server', 8443)) as sock:
        with context.wrap_socket(sock, server_hostname='server') as ssock:
            payload = {"message": "healthcheck"}
            ssock.send(json.dumps(payload).encode())
            print("T1. Sent healthcheck to server")

            response = ssock.recv(2048)
            response_data = json.loads(response.decode())
            if response_data.get("status") == "ok":
                print("R1. Healthcheck successful:", response_data)
            else:
                print("R1. Healthcheck failed:", response_data)

with socket.create_connection(('server', 8443)) as sock:
    with context.wrap_socket(sock, server_hostname='server') as ssock:
        payload = {"message": "exit"}
        ssock.send(json.dumps(payload).encode())
        print("T1. Sent exit to server")
