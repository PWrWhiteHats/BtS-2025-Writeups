#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 1;
    }

    setuid(0);
    system(argv[1]);
    return 0;
}