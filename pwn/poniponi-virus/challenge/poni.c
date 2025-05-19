#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <fcntl.h>

// I heard you like PONIPONI so I put PONI in your PONI! 🐎🐎🐎
#define PONI write(1, poni, 4);
#define PONI_1 PONI
#define PONI_2 PONI_1 PONI
#define PONI_3 PONI_2 PONI
#define PONI_4 PONI_3 PONI
#define PONI_5 PONI_4 PONI
#define PONI_6 PONI_5 PONI
#define PONI_7 PONI_6 PONI
#define PONI_8 PONI_7 PONI
#define PONI_9 PONI_8 PONI
#define PONI_10 PONI_9 PONI
#define PONIPONI(N) PONI_##N

#define BUF_SIZE 0x10

const char *text_colors[] = {
    "\033[31m",
    "\033[32m",
    "\033[33m",
    "\033[34m",
    "\033[35m",
    "\033[36m",
    "\033[37m",
    "\033[1;31m",
    "\033[1;32m",
    "\033[1;33m",
    "\033[1;34m",
    "\033[1;35m",
    "\033[1;36m",
    "\033[1;37m",
};

const char *bg_colors[] = {
    "\033[48;5;196m",
    "\033[48;5;82m",
    "\033[48;5;226m",
    "\033[48;5;21m",
    "\033[48;5;201m",
    "\033[48;5;51m",
    "\033[48;5;232m",
    "\033[48;5;15m",
};

const char *text_styles[] = {
    "\033[4m",
    "\033[5m",
    "\033[1m",
};

void make_me_a_ctf_challenge(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int random_choice(int max) {
    return rand() % max;
}

int main() {
    char poni[] = "poni";
    make_me_a_ctf_challenge();
    srand(time(NULL));
    for (int i = 0; i < 48; ++i) {
        size_t text_choices_n = sizeof text_colors / sizeof text_colors[0];
        size_t bg_choices_n = sizeof bg_colors / sizeof bg_colors[0];
        size_t style_choices_n = sizeof text_styles / sizeof text_styles[0];
        const char *text_color = text_colors[random_choice(text_choices_n)];
        const char *bg_color = bg_colors[random_choice(bg_choices_n)];
        const char *style = text_styles[random_choice(style_choices_n)];

        printf("%s%s%s", text_color, bg_color, style);
        PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);
        PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);
        PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);PONIPONI(10);
        usleep(75000);
    }
    puts("!!!");

    int ponifile = open("/proc/self/mem", 2);
    // Incrementing poni_counter... PONI_PONI_OVERFLOW! 🦄
    // Seven is a lucky number.
    for (int poni_counter = 0; poni_counter < 0x700; ++poni_counter) {
        usleep(10000);
        
        size_t len = sizeof poni - 1;
        char to_write = len;
        write(1, poni, to_write);
        
        int size = BUF_SIZE;
        char s[BUF_SIZE] = {};
        char to_read = size - 1;
        read(0, s, to_read);
        
        long n = strtol(s, NULL, 10);
        if (n == 0xc0ffee)
            break;
        
        // Error: Too many ponis on the stack. Switching to heap allocation.
        char *h = malloc(0);
        // Poni-ter arithmetic detected! (poni++)^10
        lseek(ponifile, ((size_t)h + n), SEEK_SET);
        if (write(ponifile, "poni", 4) == -1) {
            puts("I just don't know what went wrong... :<");
        }
    }
    
    return 0;
}
