#!/bin/bash

tshark -r ../challenge/logs/traffic.pcap -V -x -q \
    -o "tls.debug_file:ssldebug.log" \
    -o "tls.desegment_ssl_records: TRUE" \
    -o "tls.desegment_ssl_application_data: TRUE" \
    -o "tls.keys_list:../challenge/certs/self-signed.key" \
    -o "tls.keylog_file:../challenge/logs/ssl_keylog" \
    -Y "http"

# grep  "decrypted app data" ssldebug.log