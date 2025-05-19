CERT_DIR=./certs
KEY_FILE=$(CERT_DIR)/self-signed.key
CERT_FILE=$(CERT_DIR)/self-signed.crt
OPENSSL_CONFIG=$(CERT_DIR)/openssl.cnf
DAYS=365
BITS=4096

all: certificate monitor

.PHONY: certificate
certificate: $(KEY_FILE) $(CERT_FILE)

$(KEY_FILE) $(CERT_FILE): $(OPENSSL_CONFIG)
	mkdir -p $(CERT_DIR)
	openssl req -x509 -nodes -days $(DAYS) -newkey rsa:$(BITS) -keyout $(KEY_FILE) -out $(CERT_FILE) -config $(OPENSSL_CONFIG)

.PHONY: monitor
monitor: certificate
	mkdir -p logs
	touch logs/traffic.pcap
	python dhgen.py
	docker compose build > /dev/null
	docker compose up

.PHONY: clean
clean:
	rm -f $(KEY_FILE) $(CERT_FILE)
	rm -f logs/traffic.pcap
	rm -f logs/ssl_keylog
	rm -f ssldebug.log
	rm -f .env