#include "idt.h"

extern void pit_handler_asm();

struct idt_entry_t idt_table[IDT_SIZE];
struct idt_pointer_t idt_ptr;

static void initialize_idt_pointer()
{
    idt_ptr.limit = (sizeof(struct idt_entry_t) * IDT_SIZE) - 1;
    idt_ptr.base = (unsigned int)&idt_table;
}

static void initialize_pic()
{
    outb(PIC_1_CTRL, 0x11);
    outb(PIC_2_CTRL, 0x11);

    outb(PIC_1_DATA, 0x20);
    outb(PIC_2_DATA, 0x28);

    outb(PIC_1_DATA, 0x04);
    outb(PIC_2_DATA, 0x02);

    outb(PIC_1_DATA, 0x01);
    outb(PIC_2_DATA, 0x01);

    outb(PIC_1_DATA, 0b11111110);
    outb(PIC_2_DATA, 0xff); 

}

void load_idt_entry(int isr_number, unsigned long base, short int selector, unsigned char flags)
{
    idt_table[isr_number].offset_lowerbits = base & 0xFFFF;
    idt_table[isr_number].offset_higherbits = (base >> 16) & 0xFFFF;
    idt_table[isr_number].selector = selector;
    idt_table[isr_number].flags = flags;
    idt_table[isr_number].zero = 0;
}

void idt_init()
{
    initialize_pic();
    initialize_idt_pointer();

    load_idt_entry(32, (unsigned long)pit_handler_asm, 0x08, 0x8E); // IRQ0
    load_idt(&idt_ptr);
}
