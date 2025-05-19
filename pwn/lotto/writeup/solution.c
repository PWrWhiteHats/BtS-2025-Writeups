#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/param.h>
#include <sys/random.h>
#include <unistd.h>
/*
 * 12 9 24 37 20 25
 * aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
 */
int main() {

  unsigned int tab[6] = {};
  // "aaaa" in hex
  srand(0x61616161);
  for (int i = 0; i < 6; ++i) {
    tab[i] = rand() % 49 + 1;
  }
  for (int i = 0; i < 6; ++i) {
    printf("%u ", tab[i]);
  }
  for (int i = 0; i < 300; ++i) {
    putc('a',stdout);
  }

  putc('\n',stdout);
}
