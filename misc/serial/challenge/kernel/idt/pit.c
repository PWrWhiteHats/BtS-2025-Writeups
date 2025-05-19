#include "pit.h"

#define PIT_CHANNEL0 0x40
#define PIT_COMMAND 0x43
#define PIT_FREQUENCY 1193182
#define PIT_HZ 1000000

#define PIT_BASE 1
static int ticks = 0;

const char *bts_message = "just dont use the disabl3pic command ";
const char *bts_morse = ".--- ..- ... - / -.. --- -. - / ..- ... . / - .... . / -.. .. ... .- -... .-.. ...-- .--. .. -.-. / -.-. --- -- -- .- -. -.. ";

#define DOT_LENGTH 10
#define DASH_LENGTH 24
#define SPACE_LENGTH 48

int i = 0;
int current_delay = 0;

void pit_handler()
{
    ticks++;

    char current_char = bts_morse[i];
    if (ticks >= PIT_BASE) {
        ticks = 0;

        if (current_delay == 0) {
            sprintc(0x01);
            i++;

            if (bts_morse[i] == '\0') {
                i = 0;
            }

            current_char = bts_morse[i];

            if (current_char == ' ') {
                current_delay = SPACE_LENGTH;
            } else if (current_char == '.') {
                current_delay = DOT_LENGTH;
            } else if (current_char == '-') {
                current_delay = DASH_LENGTH;
            } else {
                current_delay = SPACE_LENGTH;
            }
        } else {
            current_delay--;
        }
    }

    outb(0x20, 0x20);
}
void pit_init()
{
    int divisor = PIT_FREQUENCY / PIT_HZ;

    outb(PIT_COMMAND, 0x36);
    outb(PIT_CHANNEL0, divisor & 0xFF);
    outb(PIT_CHANNEL0, (divisor >> 8) & 0xFF);
}
