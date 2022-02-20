#!/bin/bash
python3 -m venv env
source env/bin/activate
echo "active python binary:"
which python # validation
pip install -r requirements.txt

echo "generating RSA-4096 private/public keys and certs"
mkdir -p keys
cd keys
rm -rf *
#private key - PEM PKCS#8
openssl genpkey -out rsakey -algorithm RSA -pkeyopt rsa_keygen_bits:4096
#public key - PEM PKCS#8
openssl rsa -in rsakey -pubout -outform PEM -out rsakey.pub
#creating certificate signing request
openssl req -new -key rsakey -out keycloak-playground.csr -subj "/C=US/ST=X/L=X/O=Playground/OU=Keycloak/CN=keycloak.playground"
# check CSR
openssl req -text -noout -verify -in keycloak-playground.csr

mkdir -p ca
#private key/cert for the CA - PEM PKCS#8
openssl req -x509 -days 365 -newkey rsa:4096 -keyout ca/ca_key -out ca/ca.crt -passout pass:supersecure -subj "/C=HU/ST=Y/L=Y/O=Playground/OU=CA/CN=ca.ex"
#create cert from crs by CA
openssl x509 -req -in keycloak-playground.csr -days 365 -CA ca/ca.crt -CAkey ca/ca_key -passin pass:supersecure -CAcreateserial -out kc.crt
#check cert/CA is the issuer/ keycloak.playground subject
openssl x509 -in kc.crt -text -noout
