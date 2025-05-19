import sys

a = sys.stdin.buffer.readline()
key = 80
static = 0b01110110
for x in a:
    if x > 0x7F:
        x -= 0xA0
    key = x ^ key
    out = key ^ static
    sys.stdout.buffer.write(out.to_bytes())
