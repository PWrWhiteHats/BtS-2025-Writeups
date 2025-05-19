key = "12J4CEK"

y = ord(key[-1])
val = ord(key[-1]) & 1
for x in key[:-1]:
    y ^= ord(x)
    val *= 2
    val |= ord(x) & 1
print(key + chr(y))
print(val)
