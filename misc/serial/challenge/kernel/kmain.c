#include "stdlib.h"

#include "idt/idt.h"
#include "../serial/uart.h"

const int buffer_size = 256;
int pic_enabled = 1;

char* flag = "BtSCTF{qemu_mprint_s000_eassssy_isnt_it}";

void method() {
    sprint(">>== 华威超级开关 Huei-wei NetworkSWE v1.00 ==<<\n");
    sprint(">>== 由华威网络安全实验室开发help ==<<\n");
    sprint("<观点view>");
}

void mprint(char* buffer) {
    char* address_str = strchr(buffer, ' ');
    
    if (address_str != NULL) {
        address_str++;
        
        unsigned int address = hex_to_address(address_str);
        
        char* mem_ptr = (char*)address;
        
        sprint("[!] Memory dump:\n");
        for (int i = 0; i < 0x100; i++) {
            if (i % 16 == 0) {
                sprint("\n");
                sprinth((unsigned int)(mem_ptr + i));
                sprint(": ");
            }
            sprintc((char)*(mem_ptr + i));
            sprint(" ");
        }

    } else {
        sprint("Invalid command format. Use: mprint <address>\n");
    }
}

void kmain(unsigned int multiboot_info_address)
{
    idt_init();

    char buffer[buffer_size];
    int i = 0;

    void* func = (void*) method;

    char c;
    while (1)
    {
        c = sread();
        if (c == '\n')
        {
            buffer[i] = '\0';

            if (strcmp(buffer, "") == 0) {
                sprint("\n");
                sprint(">>== 华威超级开关 Huei-wei NetworkSWE v1.00 ==<<\n");
                sprint(">>== 由华威网络安全实验室开发help ==<<\n");
                sprint("<观点view>");
                i = 0;
                continue;
            }

            if (strcmp(buffer, "disabl3pic") == 0)
            {
                pic_enabled = 0;
                sprint("!!! 警告: PIC锁定已关闭\n");
                sprint("<观点view> 控制台管理员模式已开启... 输入 'help' 获取帮助\n");
                outb(PIC_1_DATA, 0xFF);
                outb(PIC_2_DATA, 0xFF);
            }
            else if (strcmp(buffer, "enabl3pic") == 0)
            {
                pic_enabled = 1;
                sprint("<观点view> 系统安全模式已启用 (PIC 锁定恢复)\n");
                outb(PIC_1_DATA, 0x00);
                outb(PIC_2_DATA, 0x00);
            }
            else if (strstartswith(buffer, "ip") == 0)
            {
                sprint("当前IP地址:10.0.0.10\n");
                sprint("☕️ 抱歉，这台机子只喝电，不喝咖啡。\n");
            }
            else if (strstartswith(buffer, "ping") == 0)
            {
                sprint("当前IP地址:10.0.0.10\n");
                sprint("ping-ng当前不支持指定程error序您没有互联网连接。\n");
            }

            if (pic_enabled == 1)
            {
                if (strcmp(buffer, "help") == 0)
                {
                    sprint("欢迎使用 华威超级开关 Huei-wei NetworkSWE v1.00\n");
                    sprint(">> 可用命令:\n");
                    sprint(" - flag : 获取系统状态\n");
                    sprint(" - help : 显示用户手册\n");
                    sprint(" - ip : 显示当前IP地址\n");
                    sprint(" - ping : 测试网络连接\n");
                }
                else if (strcmp(buffer, "flag") == 0)
                {
                    sprint("galf a ton si siht");
                    sprint("\n");
                }
            }

            if (pic_enabled == 0)
            {
                if (strcmp(buffer, "help") == 0)
                {
                    sprint(">> 管理员模式命令:\n");
                    sprint(" - disabl3pic : 关闭保护模式 PIC\n");
                    sprint(" - enabl3pic : 返回安全状态\n");
                    sprint(" - help : 获取命令帮助\n");
                    sprint(" - dumpmem : 内存分析工具\n");
                    sprint(" - peekmem <a> : 查看内存地址 <a>\n");
                }
                else if (strstartswith(buffer, "dumpmem"))
                {
                    sprint(">>== 内存扫描器 MEMORY SCANNER ==<<\n");
                    sprint(" - @代码段 text: ");
                    sprinth((unsigned int)&section_start_text);
                    sprint("\n");
                    sprint(" - @数据段 data: ");
                    sprinth((unsigned int)&section_start_data);
                    sprint("\n");
                    sprint(" - @未初始化数据段 bss: ");
                    sprinth((unsigned int)&section_start_bss);
                    sprint("\n");
                }
                else if (strstartswith(buffer, "peekmem"))
                {
                    mprint(buffer);
                }
            }

            sprint("\n");
            sprint("<观点view>");
            i = 0;
            continue;
        }
        if (i < buffer_size - 1)
        {
            buffer[i++] = c;
        }
    }
}
