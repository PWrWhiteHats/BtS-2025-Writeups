from pwn import ELF, xor

elf = ELF("a.out")
enc_sections = (b.data() for b in elf.sections if b.name.startswith("f_"))
print("".join(reversed([chr(xor(section, 0x55)[0]) for section in enc_sections])))
