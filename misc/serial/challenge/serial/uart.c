#include "uart.h"

void sprintc(char c) {
    while ((inb(COM1 + 5) & 0x20) == 0);
    outb(COM1, c);
}

void sprint(const char* str) {
    while (*str) {
        sprintc(*str++);
    }
}

void sprinti(int num) {
    char buf[12];
    int i = 0;
    if (num < 0) {
        sprintc('-');
        num = -num;
    }
    if (num == 0) {
        sprintc('0');
        return;
    }
    while (num > 0) {
        buf[i++] = '0' + (num % 10);
        num /= 10;
    }
    while (i--) {
        sprintc(buf[i]);
    }
}

void sprinth(int num) {
    sprint("0x");
    for (int i = 28; i >= 0; i -= 4) {
        int digit = (num >> i) & 0xF;
        if (digit < 10)
            sprintc('0' + digit);
        else
            sprintc('a' + digit - 10);
    }
}

void sprintf_impl(const char *fmt, uint32_t *args, int arg_count) {
    int arg_index = 0;
    while (*fmt) {
        if (*fmt == '%' && *(fmt + 1)) {
            fmt++;
            switch (*fmt) {
                case 'd':
                    if (arg_index < arg_count) sprinti(args[arg_index++]);
                    break;
                case 'x':
                    sprintc('0');
                    sprintc('x');
                    if (arg_index < arg_count) sprinth(args[arg_index++]);
                    break;
                case 'c':
                    if (arg_index < arg_count) sprintc((char)args[arg_index++]);
                    break;
                default:
                    sprintc('%');
                    sprintc(*fmt);
                    break;
            }
        } else {
            sprintc(*fmt);
        }
        fmt++;
    }
}

int sda() {
    return (inb(COM1 + 5) & 0x01) != 0;
}

char sread() {
    while (!sda());
    return inb(COM1);
}