#ifndef KERNEL_STDLIB_H
#define KERNEL_STDLIB_H

#include "types.h"

int strcmp(const char *str1, const char *str2) {
    while (*str1 && (*str1 == *str2)) {
        str1++;
        str2++;
    }

    return (unsigned char)*str1 - (unsigned char)*str2;
}

char* strchr(const char* str, char c) {
    while (*str) {
        if (*str == c) {
            return (char*)str;
        }
        str++;
    }
    return NULL;
}

int strstartswith(const char *str, const char *prefix) {
    while (*prefix) {
        if (*str != *prefix) {
            return 0;
        }
        str++;
        prefix++;
    }
    return 1;
}

unsigned int hex_to_address(const char *str) {
    unsigned int address = 0;
    while (*str) {
        address *= 16;
        if (*str >= '0' && *str <= '9') {
            address += *str - '0';
        } else if (*str >= 'a' && *str <= 'f') {
            address += *str - 'a' + 10;
        } else if (*str >= 'A' && *str <= 'F') {
            address += *str - 'A' + 10;
        }
        str++;
    }
    return address;
}

#endif // KERNEL_STDLIB_H