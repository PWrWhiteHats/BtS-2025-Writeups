# Roulette
*I bet a flag you can't win with a number 13 37 times in a row!*

## Overview
The challenge is a provable fair roulette game. User can choose their own client key and place a bet.
The goal is to win 37 times in a row betting 13 every time, then the flag is printed.

## Solution
The first important thing to notice is server seed generation:
```python
server_seed = sha256(bytes(secrets.randbits(17))).hexdigest()
```

Which has very little possibilities - 2^17, which is 131072, easy to bruteforce.

Then, using the user-specified seed and server seed, a number to be guessed is generated: 
```python
        # Generate game hash
        combined = f"{server_seed}:{client_seed}"
        game_hash = sha256(combined.encode()).hexdigest()
        hash_int = int(game_hash, 16)

        # Calculate roulette result
        roulette_number = hash_int % 37  # 0-36
```

So we can generate every possible server seed, and then check which client key will result in our target:
```python
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
```

Then we send computed winning client seed and number 13,
which is what we bet in order to win the challenge:
```python
conn.send(client_seed.encode() + b'\n')
conn.send(b'13\n')
```

Repeat this 37 times and print the flag that we got.


### Full solution code
```python
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

```
