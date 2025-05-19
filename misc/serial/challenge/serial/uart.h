#ifndef SERIAL_UART_H
#define SERIAL_UART_H

#include "../kernel/types.h"
#include "../kernel/x86.h"

#define COM1 0x3F8

#define sprintf(fmt, ...) \
    do { \
        uint32_t args[] = { __VA_ARGS__ }; \
        sprintf_impl(fmt, args, sizeof(args) / sizeof(args[0])); \
    } while (0)
    
void sprintc(char c);
void sprinth(int num);
void sprinti(int num);
void sprint(const char* str);
void sprintf_impl(const char *fmt, uint32_t *args, int arg_count);
char sread();

static int sda();

#endif // SERIAL_SERIAL_H