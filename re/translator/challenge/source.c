#include <locale.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <wchar.h>
uint8_t calc(unsigned char *str) {
  if (*str == '\0') {
    return 0;
  }
  return calc(str + 1) + (*str >> 4);
}

int main(int argc, char **argv) {
  setlocale(LC_ALL, "");
  if (argc != 2) {
    fprintf(stderr, "USAGE: %s <text>\n", *argv);
    return 1;
  }
  if (*argv[1] == '\0') {
    putwc('\n', stdout);
    exit(0);
  }
  uint8_t off = calc(argv[1]);
  int low = (int)argv[1][1] + off & 0xF | (int)argv[1][1] & 0xF0;
  int high = (int)*argv[1] + (off >> 4) & 0xF | (int)*argv[1] & 0xF0;
  wchar_t o = high * 0x100 + low + 0x1000;
  putwc(o, stdout);

  if (argv[1][1] == '\0') {
    putwc('\n', stdout);
    exit(0);
  }//printf("%d\n", off);
  argv[1] += 2;
  main(argc, argv);
}
