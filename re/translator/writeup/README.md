# translator

This challenge provides a program called translator that transforms a string of ASCII characters into a string of Unicode symbols.

In summary, the program "loops" (recursively) over each pair of characters from the input, performs some calculations on them, and merges them into a single Unicode character. (eg. 0x3a,0x44 -> 0x3a44). 

At the beginning of each loop, a function is called to calculate an offset value for the current Unicode character. 
After cleaning and reversing the decompiler output, the function should look like this:
```c
uint8_t fun(char *str) {
  if (*str == '\0') {
    return 0;
  }
  return fun(str + 1) + (*str >> 4);
}
```

The offset calculation starts from the currently encoded pair of character and does not include the any characters before it — giving us brute-force potential.
```c
    uint8_t offset = fun(argv[1])
    ...
    argv[1] += 2;
    main(2,argv);
```
Note: To save function call, the compiler made the code to compute the offset starting from the second character and add the result of the first one manually afterwards. This doesn't change any logic so I will skip over it.
```c
    uint8_t out = fun(argv[1] + 1)
    uint8_t offset = out + (*argv[1] >> 4)
```

### Bruteforce solution
A straightforward solution is to just brute-force the flag. However, there are two caveats:
- Because of how the offset is generated, we must brute-force backwards.
- The number of characters in the flag is odd, so for the last pair, the second character is `\0`. 

Code for the bruteforce solution:
```py
import subprocess
import string
from itertools import product

charset = string.printable.strip()
program_path = './translator'
secret = '幾湂潌蕔䩘桢豝詧䭡䝵敯䡨剱挧䍩硷穏罣㈡䨥'
found = '}'
for i in range(len(secret) - 1, -1, -1):
    print(f"target: '{secret[i]}'")
    for a, b in product(charset, repeat=2):
        result = subprocess.run([program_path, a + b + found], capture_output=True, text=True, timeout=1)
        if result.stdout.strip()[0] == secret[i]:
            print(f"found: '{a}{b}' -> '{secret[i]}'")
            found = a + b + found
            break
final_input = ''.join(found)
print(f"out: {final_input}")
```

### Reverse Engineering Solution
Second, RE/"intended" solution is more time-consuming but not particularly complicated. Below is a cleaner version of the decompiler output.
```c
  // first_byte = *argv[1]
  // second_byte = argv[1][1]
  uint8_t offset = fun(first_byte)
  ... 
  int high_byte = (first_byte & 0xF0) | (first_byte + (offset >> 4) & 0xF);
  int low_byte = (second_byte & 0xF0) | (second_byte + offset & 0xF);
  wchar_t o = high * 0x100 + low + 0x1000;
  putwc(o, stdout);
```
Graphical representation of the translation process:
```
->{ 0x42   4 +
  { 0x74   7 + 
    0x53   5 + 
    0x42   4 + 
    ...   ...+ 
    0x5a   5 + 
    0x00   0 % 0xFF = 0xCA (offset)
    
           0xCA \/ 
    0x42 -> 2 + C -> 0x4E
    0x74 -> 4 + A -> 0x7E
    
    0x4E * 0x100 + 0x7E = 0x4E7E 
    0x4E7E + 0x1000 = 0x5E7E = 幾
```
Code for the RE solution:
```py
inp = '幾湂潌蕔䩘桢豝詧䭡䝵敯䡨剱挧䍩硷穏罣㈡䨥贇'

def sub_with_roll(x, offset):
    if offset > x & 0xF:
        return (x & 0xF0) + ((x & 0xF) - offset + 0x10)
    else:
        return x - offset

for i, x in enumerate(inp):
    offset = 0
    for j in range(i, len(inp)):
        offset += ((ord(inp[j]) - 0x1000) >> 4) & 0xF
        offset += ((ord(inp[j]) - 0x1000) >> 12) & 0xF
    y = hex(ord(x) - 0x1000)
    low = sub_with_roll(int(y[4:6], 16), offset & 0xF)
    high = sub_with_roll(int(y[2:4], 16), (offset >> 4) & 0xF)
    print(chr(high) + chr(low), end='')
```
