import sys

a = input()
key = 99
static = 0b01110110
for x in a:
    out = ord(x) ^ static ^ key
    key = ord(x) ^ static
    if out < 0x20:
        out += 0xA0
    sys.stdout.buffer.write(out.to_bytes())
