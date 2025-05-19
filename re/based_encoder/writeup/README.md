# Solution

Flag is a base64 encoded string in a binary, thus the solution is:

```sh
strings based_encoder | tail -n 5 | head -n 1 | cut -d '.' -f 2 | base64 -d | ./based_encoder
```
