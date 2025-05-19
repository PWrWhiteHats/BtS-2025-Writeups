#ifndef KERNEL_TYPES_H
#define KERNEL_TYPES_H

#define NULL 0

typedef unsigned char uint8_t;
typedef unsigned short uint16_t;
typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;
typedef unsigned long size_t;

extern uint32_t stack_begin;
extern uint32_t stack_end;
extern uint32_t section_start_text;
extern uint32_t section_end_text;
extern uint32_t section_start_data;
extern uint32_t section_end_data;
extern uint32_t section_start_bss;
extern uint32_t section_end_bss;
extern uint32_t flag_start;
extern uint32_t flag_end;

#endif // KERNEL_TYPES_H