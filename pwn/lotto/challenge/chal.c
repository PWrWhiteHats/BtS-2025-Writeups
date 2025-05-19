#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/param.h>
#include <sys/random.h>
#include <unistd.h>
#pragma pack(1)
#define WELCOMEMESSEGE                                                         \
  "    .____           __    __          \n"                                   \
  "    |    |    _____/  |__/  |_  ____  \n"  \ 
 "    |    |   /  _ \\   __\\   __\\/    \\ \n"                                \
 "    |    |__(  <_> )  |  |  | (  <_> )\n"                                    \
 "    |_______ \\____/|__|  |__|  \\____/ \n"                                  \
 "            \\/                        \n"                                   \
 "    Enter 6 numbers in range 1 to 49   \n"

#define FAILMESSEGE "    Better luck next time ;)  \n"
#define CORRECTNUMBERSMESSEGE "    Number of correct guesses: "

unsigned userLookup[49] = {};
unsigned winingLookup[49] = {};
unsigned winingNumbers[6] = {};
typedef struct {
  unsigned int correctNumbers;
  char userInput[32];
  char welcomeMessegeBuffer[sizeof(WELCOMEMESSEGE)];
  unsigned int seed;
  char failMessegeBuffer[sizeof(FAILMESSEGE)];
  char correctNumbersMessegeBuffer[sizeof(CORRECTNUMBERSMESSEGE)];

} lottoData;
int main() {
  lottoData lotto = {};
  unsigned userNumbers[6] = {};
  lotto.seed = 0;
  getrandom(&lotto.seed, sizeof(lotto.seed), 0);
  memcpy(lotto.welcomeMessegeBuffer, WELCOMEMESSEGE, sizeof(WELCOMEMESSEGE));
  memcpy(lotto.failMessegeBuffer, FAILMESSEGE, sizeof(FAILMESSEGE));
  memcpy(lotto.correctNumbersMessegeBuffer, CORRECTNUMBERSMESSEGE,
         sizeof(CORRECTNUMBERSMESSEGE));
  setbuf(stdout, NULL);
  printf("%s\n    ", lotto.welcomeMessegeBuffer);
  char input[sizeof(lottoData)] = {};
  fgets(input, sizeof(lottoData), stdin);
  memcpy(lotto.userInput, input, strlen(input));
  srand(lotto.seed);
  sscanf(lotto.userInput, "%u %u %u %u %u %u", &userNumbers[0], &userNumbers[1],
         &userNumbers[2], &userNumbers[3], &userNumbers[4], &userNumbers[5]);
  for (int i = 0; i < 6; ++i) {
    winingNumbers[i] = rand() % 49 + 1;
  }
  for (int i = 0; i < 6; ++i) {
    userLookup[userNumbers[i]]++;
    winingLookup[winingNumbers[i]]++;
  }
  for (int i = 0; i < 49; ++i) {
    if (userLookup[i] > 0 && winingLookup[i] > 0) {
      lotto.correctNumbers += MIN(userLookup[i], winingLookup[i]);
    }
  }

  if (lotto.correctNumbers == 6) {
    system("cat flag");

  } else {
    printf("%s%u\n", lotto.correctNumbersMessegeBuffer, lotto.correctNumbers);
    printf("%s\n", lotto.failMessegeBuffer);
  }
}
