#ifndef KERNEL_IDT_ISR_H
#define KERNEL_IDT_ISR_H

void pit_handler();

__attribute__((naked)) void pit_handler_asm()
{
    __asm__ volatile(
        "pusha\n\t"
        "call pit_handler\n\t"
        "popa\n\t"
        "iret\n\t");
}

#endif // KERNEL_ISR_H
