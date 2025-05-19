# Healthcheck

## Solution

The program does not check if rdseed failed.

Thus all we need to do is request encrypted flags, and
try to decrypt them with key: 0, until we succeed.

Running the solution:

## How to run

The script, by default, will send requests to <http://localhost:1337/flags>. You may need to adjust it.

```sh
cargo run
```
