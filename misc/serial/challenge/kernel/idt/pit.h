#ifndef KERNEL_IDT_PIT_H
#define KERNEL_IDT_PIT_H

#include "../x86.h"
#include "../types.h"
#include "../../serial/uart.h"

#include "isr.h"

void pit_init();
void pit_handler();

#endif // KERNEL_IDT_PIT_H