#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

int FILES[0x10];
char *PATHS[0x10];

void menu(void) {
    puts("1. list opened files");
    puts("2. open a new file");
    puts("3. close a file");
    puts("4. exit");
    puts("");
}

int read_number(void) {
    char line[100] = {};
    scanf("%99s", line);
    
    char *endptr;
    long number;
    number = strtol(line, &endptr, 10);
    if (endptr == line || *endptr != '\n' && *endptr != '\0') {
        printf("not a number: %s\n", line);
        exit(-3);
    }

    return number;
}

void list_files(void) {
    for (int i = 0; i < 0x10; ++i) {
        int file = FILES[i];
        char *path = PATHS[i];
        if (file == -1)
            continue;
        printf("%d: %s\n", file, path);
    }
}

void close_file(void) {
    printf("fd to close: ");
    int fd = read_number();
    if (fd == -1)
        return;
    close(fd);
    for (int i = 0; i < 0x10; ++i) {
        if (FILES[i] == fd) {
            FILES[i] = -1;
            free(PATHS[i]);
            PATHS[i] = 0;
        }
    }
}

void open_file(void) {
    char *path = calloc(1, 100);
    if (path == 0) {
        puts("something went very wrong, contact admins");
        exit(-1);
    }

    printf("enter file path: ");
    scanf("%99s", path);

    int fd = open(path, O_RDONLY);
    for (int i = 0; i < 0x10; ++i) {
        if (FILES[i] == -1) {
            FILES[i] = fd;
            PATHS[i] = path;
            break;
        }
    }
}

int main() {
    for (int i = 0; i < 0x10; i++) {
        FILES[i] = -1;
    }
    setvbuf(stdout, NULL, _IOLBF, 0);
    setvbuf(stdin, NULL, _IOLBF, 0);
    setvbuf(stderr, NULL, _IOLBF, 0);
    _Bool quit = 0;

    while (!quit) {
        menu();
        int number = read_number();

        switch (number) {
            case 1:
                list_files();
                break;
            case 2:
                open_file();
                break;
            case 3:
                close_file();
                break;
            case 4:
                quit = 1;
                break;
        }
    }

    return 0;
}
