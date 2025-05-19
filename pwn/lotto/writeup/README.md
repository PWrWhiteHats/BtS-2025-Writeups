# Write-up
```c
typedef struct {
  unsigned int correctNumbers;
  char userInput[32];
  char welcomeMessegeBuffer[sizeof(WELCOMEMESSEGE)];
  unsigned int seed;
  char failMessegeBuffer[sizeof(FAILMESSEGE)];
  char correctNumbersMessegeBuffer[sizeof(CORRECTNUMBERSMESSEGE)];

} lottoData;
... 
getrandom(&lotto.seed, sizeof(lotto.seed), 0);
...
char input[sizeof(lottoData)] = {};
fgets(input, sizeof(lottoData), stdin);
memcpy(lotto.userInput, input, strlen(input));
srand(lotto.seed);
```
The fgets function reads user input into a buffer (input) sized to hold the entire lottoData structure, not just the lotto.userInput field. <br>
This allows user input exceeding the size of lotto.userInput to overflow into subsequent fields within the lottoData structure, including the seed. <br>
By providing carefully crafted input, an attacker can overwrite the seed, before generator has been seeded with a proper random seed.
<br> 
This allows them to calculate the winning numbers beforehand, since they controll the seed.

