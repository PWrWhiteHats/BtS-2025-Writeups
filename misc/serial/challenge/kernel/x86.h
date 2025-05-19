#ifndef KERNEL_X86_H
#define KERNEL_X86_H

static inline void outb(unsigned short port, unsigned char value)
{
    __asm__ volatile("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline unsigned char inb(unsigned short port)
{
    unsigned char ret;
    __asm__ volatile("inb %1, %0" : "=a"(ret) : "Nd"(port));
    return ret;
}

static inline void load_idt(void *idt_ptr)
{
    __asm__ volatile("lidt (%0); sti" : : "r"(idt_ptr) : "memory");
}

#endif // KERNEL_X86_H