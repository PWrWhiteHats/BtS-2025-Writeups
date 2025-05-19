from sympy import randprime
from math import isqrt
import random
import os

N_FACTORS = 6
FACTOR_BITS = 64
L_BITS = 1024

def generate_weak_prime(bits=L_BITS, factor_bits=FACTOR_BITS):
    small_factors = [randprime(2**(factor_bits-1), 2**factor_bits) for _ in range(N_FACTORS)]
    p = 1
    for f in small_factors:
        p *= f
    return p

def generate_bad_generator(p):
    return random.randint(2, 20)

def generate_faulty_dh():
    p = generate_weak_prime(L_BITS, FACTOR_BITS)

    g = generate_bad_generator(p)

    a = random.randint(2, isqrt(p))
    b = random.randint(2, isqrt(p))

    A = pow(g, a, p)
    B = pow(g, b, p)

    return p, g, a, A, b, B

p, g, a, A, b, B = generate_faulty_dh()

with open(".env", "w") as env_file:
    env_file.write(f"DH_MODULUS={p}\n")
    env_file.write(f"DH_GENERATOR={g}\n")
    env_file.write(f"DH_PRIVKEY_CLIENT={a}\n")
    env_file.write(f"DH_PRIVKEY_SERVER={b}\n")

print(f"p = {p}")
print(f"g = {g}")
print(f"a = {a}")
print(f"A = {A}")
print(f"b = {b}")
print(f"B = {B}")
print(f"k = {pow(A, b, p)}")