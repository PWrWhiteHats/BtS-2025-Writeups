from hashlib import sha256
from pwn import *

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 13137

# generate all possible server seeds
print("Generating possible server seeds...")
poss_server_seeds = {}
for i in range(0, 2**17):
    possible_server_seed = sha256(bytes(i)).hexdigest()
    possible_server_hash = sha256(possible_server_seed.encode()).hexdigest()
    poss_server_seeds[possible_server_hash] = possible_server_seed

conn = remote(TARGET_HOST, TARGET_PORT)

for round_ in range(37):
    seed_hash_part = conn.recvuntil(b'client seed (press enter to generate): ').decode()
    lines = seed_hash_part.split('\n')
    seed_hash_line = next((line for line in lines if line.startswith("Server seed hash")))
    hash_str = seed_hash_line.split(":")[1].strip()
    guessed_server_seed = poss_server_seeds[hash_str]

    print("Hash:", hash_str)
    print("Server seed:", guessed_server_seed)

    i = 0
    while True:
        client_seed = str(i)
        # Generate game hash
        combined = f"{guessed_server_seed}:{client_seed}"
        game_hash = sha256(combined.encode()).hexdigest()
        hash_int = int(game_hash, 16)

        # Calculate roulette result
        roulette_number = hash_int % 37
        if roulette_number == 13:
            break

        i += 1
    print("Client seed:", client_seed)
    conn.send(client_seed.encode() + b'\n')
    # sleep(1)
    conn.send(b'13\n')

for line in conn.recvall().decode().split('\n'):
    if line.startswith("How? How is it possible?"):
        print(line)
