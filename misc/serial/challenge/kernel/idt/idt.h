#ifndef KERNEL_IDT__H
#define KERNEL_IDT__H

#include "../x86.h"
#include "../types.h"

#define IDT_SIZE 256
#define IDT_ENTRIES 256

#define PIC_1_CTRL 0x20
#define PIC_2_CTRL 0xA0
#define PIC_1_DATA 0x21
#define PIC_2_DATA 0xA1

struct idt_entry_t
{
    unsigned short int offset_lowerbits;
    unsigned short int selector;
    unsigned char zero;
    unsigned char flags;
    unsigned short int offset_higherbits;
} __attribute__((packed));

struct idt_pointer_t
{
    unsigned short limit;
    unsigned int base;
} __attribute__((packed));

extern struct idt_entry_t idt_table[IDT_SIZE];
extern struct idt_pointer_t idt_ptr;

void load_idt_entry(int isr_number, unsigned long base, short int selector, unsigned char flags);
void idt_init();

#endif // KERNEL_IDT__H
