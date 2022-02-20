# Keycloak playground

#HOW TO RUN
1. run init.sh, this prepares/activates the python virtual env and generates rsa keys/certs
2. cd to the given dir
3. docker-compose up
4. run the tester.py file with python3

#EXAMPLES
##service account
- service account with client secret
- service account with signed JWT/preset public key
- service account with signed JWT/JWKS URL

#DEV ENVIRONMENT
- Ubuntu 20.04 LTS
- Docker 20.10.12
- Python 3.8.10
- OpenSSL 1.1.1f  31 Mar 2020


python Keycloak admin library:
https://github.com/marcospereirampj/python-keycloak
