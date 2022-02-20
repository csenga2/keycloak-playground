import requests
import jwt
import pprint
import token_helper


class ServiceAccountHelper:
    def __init__(self, keycloak_admin, keycloak_url):
        self.keycloak_admin = keycloak_admin
        self.keycloak_url = keycloak_url

    def get_access_token_by_secret(self, realm_name, client_name, secret):
        response = requests.post(self.keycloak_url + "/realms/" + realm_name + "/protocol/openid-connect/token",
                                 data={"grant_type": "client_credentials",
                                       "client_id": client_name,
                                       "client_secret": secret})
        return response.json()['access_token']

    def create_service_account_with_client_secret(self, client_name):
        client = {
            "name": client_name,
            "clientId": client_name,
            "enabled": True,
            "serviceAccountsEnabled": True,
            "clientAuthenticatorType": "client-secret"
        }

        self.keycloak_admin.create_client(client)
        id = self.keycloak_admin.get_client_id(client_name)
        self.keycloak_admin.generate_client_secrets(id)
        secret = self.keycloak_admin.get_client_secrets(id)

        return secret["value"]

    def test_service_account_with_client_secret(self, realm_name):
        # service account with client secret
        client_name = "service-account-client-secret"
        service_account_client_secret = self.create_service_account_with_client_secret(client_name)

        token = self.get_access_token_by_secret(realm_name, client_name, service_account_client_secret)

        print()
        print("test_service_account_with_client_secret:")
        print()
        pprint.pprint(jwt.decode(token, options={"verify_signature": False}))

    def create_service_account_with_client_key(self, client_name, public_key):
        client = {
            "name": client_name,
            "clientId": client_name,
            "enabled": True,
            "serviceAccountsEnabled": True,
            "clientAuthenticatorType": "client-jwt",
            "attributes": {
                "jwt.credential.public.key": public_key,
                "use.jwks.string": False,
                "use.jwks.url": False
            }
        }

        self.keycloak_admin.create_client(client)
        id = self.keycloak_admin.get_client_id(client_name)
        self.keycloak_admin.generate_client_secrets(id)
        secret = self.keycloak_admin.get_client_secrets(id)

        return secret["value"]

    def test_service_account_with_signed_jwt_provided_by_predefined_rsa_key(self, realm_name):
        client_name = "service-account-test-rsa-key"

        with open('../keys/rsakey.pub', 'r') as file:
            public_key = file.read()
        self.create_service_account_with_client_key(client_name, public_key)

        with open('../keys/rsakey', 'r') as file:
            private_key = file.read()
        assertion_token = token_helper.create_signed_jwt(client_name, realm_name, private_key)

        response = requests.post(self.keycloak_url + "/realms/" + realm_name + "/protocol/openid-connect/token",
                                 data={"grant_type": "client_credentials",
                                       "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                                       "client_id": client_name,
                                       "client_assertion": assertion_token})
        token = response.json()['access_token']

        print()
        print("test_service_account_with_rsa_key:")
        print()
        pprint.pprint(jwt.decode(token, options={"verify_signature": False}))

    def create_service_account_with_jwks(self, client_name, jwks_url):
        client = {
            "name": client_name,
            "clientId": client_name,
            "enabled": True,
            "serviceAccountsEnabled": True,
            "clientAuthenticatorType": "client-jwt",
            "attributes": {
                "jwks.url": jwks_url,
                "use.jwks.string": False,
                "use.jwks.url": True
            }
        }

        self.keycloak_admin.create_client(client)
        id = self.keycloak_admin.get_client_id(client_name)
        self.keycloak_admin.generate_client_secrets(id)
        secret = self.keycloak_admin.get_client_secrets(id)

        return secret["value"]

    def test_service_account_with_signed_jwt_by_jwks_url(self, realm_name, remote_realm_jwks, kid):
        client_name = "service-account-test-jwks"

        self.create_service_account_with_jwks(client_name, remote_realm_jwks)

        with open('../keys/rsakey', 'r') as file:
            private_key = file.read()
        assertion_token = token_helper.create_signed_jwt_with_kid(client_name, realm_name, private_key, kid)

        response = requests.post(self.keycloak_url + "/realms/" + realm_name + "/protocol/openid-connect/token",
                                 data={"grant_type": "client_credentials",
                                       "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
                                       "client_id": client_name,
                                       "client_assertion": assertion_token})
        token = response.json()['access_token']

        print()
        print("test_service_account_with_jwks_url:")
        print()
        pprint.pprint(jwt.decode(token, options={"verify_signature": False}))
