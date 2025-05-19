#include <stdio.h>
#include <stdlib.h>
#include <memory.h>


#define MAX_DUMPS 0x41
#define MAX_DUMP_SIZE 0x4141

// Georgia 16 by Richard Sabey 8.2003
char logo[] = \
"____    ____                         ________                                                      \n"
"`MM'    `MM'                         `MMMMMMMb.                                                    \n"
" MM      MM                           MM    `Mb                                                    \n"
" MM      MM   ____  ____   ___        MM     MM ___   ___ ___  __    __  __ ____     ____  ___  __ \n"
" MM      MM  6MMMMb `MM(   )P'        MM     MM `MM    MM `MM 6MMb  6MMb `M6MMMMb   6MMMMb `MM 6MM \n"
" MMMMMMMMMM 6M'  `Mb `MM` ,P          MM     MM  MM    MM  MM69 `MM69 `Mb MM'  `Mb 6M'  `Mb MM69   \n"
" MM      MM MM    MM  `MM,P           MM     MM  MM    MM  MM'   MM'   MM MM    MM MM    MM MM'    \n"
" MM      MM MMMMMMMM   `MM.           MM     MM  MM    MM  MM    MM    MM MM    MM MMMMMMMM MM     \n"
" MM      MM MM         d`MM.          MM     MM  MM    MM  MM    MM    MM MM    MM MM       MM     \n"
" MM      MM YM    d9  d' `MM.         MM    .M9  YM.   MM  MM    MM    MM MM.  ,M9 YM    d9 MM     \n"
"_MM_    _MM_ YMMMM9 _d_  _)MM_       _MMMMMMM9'   YMMM9MM__MM_  _MM_  _MM_MMYMMM9   YMMMM9 _MM_    \n"
"                                                                          MM                       \n"
"                                                                          MM                       \n"
"                                                                         _MM_                      \n";

size_t no_dumps = 0;
void *dumps[MAX_DUMPS];
size_t dump_sizes[MAX_DUMPS];

void make_me_a_ctf_challenge(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void menu(void) {
    puts("=========== DUMP MENU ===========");
    puts("1) Create a new dump");
    puts("2) Hexdump a dump");
    puts("3) Bite a byte");
    puts("4) Merge two dumps");
    puts("5) Resize dump");
    puts("6) Remove dump");
    puts("7) Dump all dumps");
    puts("8) Dump the dump menu");
    puts("0) Coredump");
}

void create_dump(void) {
    if (no_dumps >= MAX_DUMPS) {
        puts("\tExceeded maximum dump limit!");
        return;
    }

    size_t dump_size = 0;
    printf("\tDump size: ");
    scanf("%lu", &dump_size);
    if (dump_size > MAX_DUMP_SIZE) {
        printf("\tYour dump is too big! %lu > %lu\n",
               dump_size,
               (size_t)MAX_DUMP_SIZE);
        return;
    }

    void *dump = malloc(dump_size);
    if (dump == NULL) {
        puts("Something went very wrong, contact admins");
        exit(-1);
    }
    memset(dump, 0, dump_size);
    
    size_t free_dump_idx = 0;
    while (dumps[free_dump_idx] != NULL) ++free_dump_idx;
    dumps[free_dump_idx] = dump;
    dump_sizes[free_dump_idx] = dump_size;
    ++no_dumps;

    printf("\tSuccessfully created a dump at index %lu\n", free_dump_idx);
}

int ask_for_index(void) {
    int idx = -1;

    printf("\tDump index: ");
    scanf("%d", &idx);
    if (idx >= MAX_DUMPS) {
        puts("\tIndex is too big");
        return -1;
    }

    return idx;
}

void hexdump_dump(void) {
    int idx = ask_for_index();
    if (idx == -1)
        return;

    char *dump = dumps[idx];
    if (dump == NULL) {
        printf("\tDump with index %d doesn't exist\n", idx);
        return;
    }
    size_t len = dump_sizes[idx];

    puts("");
    puts("          0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f");
    puts("     +--------------------------------------------------");
    for (size_t i = 0; i < len; ++i) {
        if (i % 16 == 0) {
            // Avoid newline for first line
            if (i != 0)
                putchar('\n');
            printf("%04lx |  ", i);
        }
        printf(" %02hhX", dump[i]);
    }
    putchar('\n');
}

void change_byte(void) {
    int idx = ask_for_index();
    if (idx == -1)
        return;
    unsigned char *dump = dumps[idx];
    if (dump == NULL) {
        printf("\tDump with index %d doesn't exist\n", idx);
        return;
    }
    size_t len = dump_sizes[idx];

    printf("\tOffset: ");
    size_t offset = 0;
    scanf("%lu", &offset);
    if (offset >= len) {
        printf("\tOffset is bigger than dump size. %lu >= %lu\n", offset, len);
        return;
    }

    printf("\tValue in decimal: ");
    unsigned char byte = 0;
    scanf("%hhu", &byte);
    dump[offset] = byte;
    printf("\tByte at offset %lu changed successfully\n", offset);
}

void merge_dumps(void) {
    int idx1 = ask_for_index();
    if (idx1 == -1)
        return;
    if (dumps[idx1] == NULL) {
        printf("\tDump with index %d doesn't exist\t", idx1);
        return;
    }
    
    int idx2 = ask_for_index();
    if (idx2 == -1)
        return;
    if (dumps[idx2] == NULL) {
        printf("\tDump with index %d doesn't exist\n", idx2);
        return;
    }

    if (idx1 == idx2) {
        puts("\tCan't merge a dump with itself");
        return;
    }

    size_t len1 = dump_sizes[idx1];
    size_t len2 = dump_sizes[idx2];
    size_t new_len = len1 + len2;
    if (new_len > MAX_DUMP_SIZE) {
        printf("\tMerged size is too big! %lu > %lu\n",
               new_len,
               (size_t)MAX_DUMP_SIZE);
        return;
    }
    dumps[idx1] = realloc(dumps[idx1], len1+len2);
    dump_sizes[idx1] = new_len;

    // Code from: https://en.wikipedia.org/wiki/Duff%27s_device
    register unsigned char *to = dumps[idx1]+len1, *from = dumps[idx2];
    register int count = len2;
    {
        register int n = (count + 7) / 8;
        switch (count % 8) {
        case 0: do { *to++ = *from++;
        case 7:      *to++ = *from++;
        case 6:      *to++ = *from++;
        case 5:      *to++ = *from++;
        case 4:      *to++ = *from++;
        case 3:      *to++ = *from++;
        case 2:      *to++ = *from++;
        case 1:      *to++ = *from++;
                } while (--n > 0);
        }
    }

    free(dumps[idx2]);
    dumps[idx2] = NULL;
    dump_sizes[idx2] = 0;
    --no_dumps;
    
    puts("\tMerge successful");
}

void resize_dump(void) {
    int idx = ask_for_index();
    if (idx == -1)
        return;
    if (dumps[idx] == NULL) {
        printf("\tDump with index %d doesn't exist\n", idx);
        return;
    }

    printf("\tNew size: ");
    size_t new_size = 0;
    scanf("%lu", &new_size);
    if (new_size > MAX_DUMP_SIZE) {
        printf("\tNew size is too big! %lu > %lu\n",
               new_size,
               (size_t)MAX_DUMP_SIZE);
        return;
    }
    
    size_t old_size = dump_sizes[idx];
    if (old_size < new_size) {
        dumps[idx] = realloc(dumps[idx], new_size);

        // Zero out the new memory
        size_t no_new_bytes = new_size - old_size;
        memset(dumps[idx]+old_size, 0, no_new_bytes);
    }
    
    dump_sizes[idx] = new_size;
    puts("\tResize successful");
}

void remove_dump(void) {
    int idx = ask_for_index();
    if (idx == -1)
        return;
    if (dumps[idx] == NULL) {
        printf("\tNo dump at index %d\n", idx);
        return;
    }

    free(dumps[idx]);
    dumps[idx] = NULL;
    dump_sizes[idx] = 0;
    --no_dumps;
    printf("\tDump at index %d removed successfully\n", idx);
}

void list_dumps(void) {
    for (int i = 0; i < MAX_DUMPS; ++i) {
        void *dump = dumps[i];
        size_t len = dump_sizes[i];
        if (dump == NULL)
            continue;
        printf("%02d: size=%lu\n", i, len);
    }
}

int main() {
    make_me_a_ctf_challenge();
    printf("%s", logo);

    menu();
    for (;;) {
        putchar('\n');
        // Remember to always check the return value of stdio.h functions kids!
        // Stay safe!
        if (printf("==> ") < 0) {
            printf("error while printing !!\n");
            exit(-1);
        }
        int option = 0;
        scanf("%d", &option);
        switch (option) {
            case 1:
                create_dump();
                break;
            case 2:
                hexdump_dump();
                break;
            case 3:
                change_byte();
                break;
            case 4:
                merge_dumps();
                break;
            case 5:
                resize_dump();
                break;
            case 6:
                remove_dump();
                break;
            case 7:
                list_dumps();
                break;
            case 8:
            default:
                menu();
                break;
            case 0:
                exit(0);
        }
    }
}
