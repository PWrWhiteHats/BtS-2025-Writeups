Writeup:
Base64 encodes binary data in 6-bit chunks. When the bit count isn't divisible by 6, the remainder of any 6 bit segment that is already being encoded will be zeroed out and zero-padding is added followedby '=' characters.
Saying so, in two-byte input (like "Th" → "VGg="), we can hide 2 extra bits in the last 6-bit block
and in one-byte input (like "T" → "VA=="), we can hide 4 extra bits
Extra bits doesn't impacts on encoded text so e.g. "Th" (01010100 01101000) can be encoded as "VGg=" (010101 000110 100000 + padding 00), "VGh=" (010101 000110 100000 + padding 01), "VGi=" (010101 000110 100000 + padding 10), "VGj=" (010101 000110 100000 + padding 11) as well. 
Padding values can be reversed to get the flag using the attached script "solution.py"