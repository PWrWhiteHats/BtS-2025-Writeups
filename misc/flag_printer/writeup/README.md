# Writeup

## Flag Printer

Non-ASCII identifiers get translated to ASCII ones in Python.
[Link to PEP 3131](https://peps.python.org/pep-3131/)

```py
if user_choice == "flag":
    print("We are sorry, but this one is currently unavailable")
    continue
```

We can bypass the first check by using any characters that are normalized to `"flag"`, e.g., `ᶠlag`.

But that's not the end of the challenge:

```py
flag = "This CTF is organized by a Polish university, we decided to switch to Polish variable names, so we moved flag to flaga"
```

Now we need to print a variable with a name that is 5 letters long, but we can only provide 4.
Thankfully, there are some characters that normalize to a different length.
It was just a matter of finding the right character — we can use a script to find such characters:

```py
import sys
import string
import unicodedata

mappings = {}

for i in range(sys.maxunicode + 1):
    c = chr(i)
    normalized_c = unicodedata.normalize('NFKC', c)
    if normalized_c != c:
        print(f"input {c} (U+{hex(i)}) is normalized to {normalized_c}")
        if normalized_c in string.printable:
            mappings.setdefault(normalized_c, []).append(c)

for normalized_c in sorted(mappings.keys()):
    unic_list = mappings[normalized_c]
    print(f"literal '{normalized_c}' can be represented by: {unic_list}")
```

<sup>[Script author](https://github.com/nikosChalk/ctf-writeups/blob/master/uiuctf22/jail/a-horse-with-no-neighs/README.md)</sup>

The right character is [ﬂ](https://www.compart.com/en/unicode/U+FB02), so our final input is `ﬂaga`.
