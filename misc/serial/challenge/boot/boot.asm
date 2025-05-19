bits   32
global start
extern kmain

global stack_begin
global stack_end

start:    
    ; Load gdtr - Global Descriptor Table Register
    lgdt [gdtr]

    jmp CODE32_SEL:.setcs
.setcs:
    ; Setup the segment registers with data selector
    mov ax, DATA32_SEL
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss,  ax
    mov esp, stack_end

    ; GRUB2 Multiboot Header Address sits in ebx register
    push ebx

    ; Call the kernel
    call kmain

endloop:
    hlt                         
    jmp endloop

; Build a GDT descriptor entry Macro
%define MAKE_GDT_DESC(base, limit, access, flags) \
    (((base  & 0x00FFFFFF) << 16) | \
    ((base   & 0xFF000000) << 32) | \
    (limit   & 0x0000FFFF) | \
    ((limit  & 0x000F0000) << 32) | \
    ((access & 0xFF) << 40) | \
    ((flags  & 0x0F) << 52))

section .data

align   4
gdt_start:
    dq MAKE_GDT_DESC(0, 0, 0, 0)
gdt32_code:
    dq MAKE_GDT_DESC(0, 0x00ffffff, 10011010b, 1100b)
gdt32_data:
    dq MAKE_GDT_DESC(0, 0x00ffffff, 10010010b, 1100b)
                               
end_of_gdt:

gdtr:
    dw end_of_gdt - gdt_start - 1
    dd gdt_start

CODE32_SEL equ gdt32_code - gdt_start
DATA32_SEL equ gdt32_data - gdt_start

section .bss

stack_begin:
    resb 4 * 32 * 1024 ; 32kiB stack
stack_end: