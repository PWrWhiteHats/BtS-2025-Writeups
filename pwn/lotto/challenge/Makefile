# LDFLAGS=-static
# chal: chal.c
# Compiler to use
CC = gcc

# Compiler flags
CFLAGS = -Wall

# Target binary
TARGET = lotto.bin

# Source file
SRC = chal.c

# Rule to build the binary
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

# Rule to clean the build
clean:
	rm -f $(TARGET)
