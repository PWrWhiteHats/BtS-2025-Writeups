CERT_DIR=../challenge
KEY_FILE=$(CERT_DIR)/self-signed.key
CERT_FILE=$(CERT_DIR)/self-signed.crt

all: solve

.PHONY: solve
solve:
	./tshark.sh
	python solve.py

.PHONY: clean
clean:
	rm -f ssldebug.log