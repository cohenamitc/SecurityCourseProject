#!/bin/bash

openssl req -x509 -nodes -days 365 -subj "/C=IL/ST=Central/L=TLV/O=CommLTD/OU=IT Department/CN=CommLTD.cyber.course" -addext "subjectAltName=DNS:CommLTD.cyber.course" -newkey rsa:2048 -keyout $SSL_CERT_DIR/server.key -out $SSL_CERT_DIR/server.crt