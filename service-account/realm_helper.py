from keycloak import KeycloakAdmin
import requests


class RealmHelper:
    def __init__(self, keycloak_admin: KeycloakAdmin, keycloak_url):
        self.keycloak_admin = keycloak_admin
        self.keycloak_url = keycloak_url

    def create_realm(self, realm_name):
        # if the realm already exists delete it
        if list(filter(lambda c: c['realm'] == realm_name, self.keycloak_admin.get_realms())):
            self.keycloak_admin.delete_realm(realm_name)

        realm = {
            "realm": realm_name,
            "enabled": True
        }
        self.keycloak_admin.create_realm(realm)

    def add_rsa_key(self, realm_name):
        realm_id = list(filter(lambda c: c['realm'] == realm_name, self.keycloak_admin.get_realms()))[0]["id"]

        with open('../keys/rsakey', 'r') as file:
            private_key = file.read()

        component = {"name": "rsa",
                      "providerId": "rsa",
                      "providerType": "org.keycloak.keys.KeyProvider",
                      "parentId": realm_id,
                      "config": {"priority": ["0"],
                                 "enabled": ["true"],
                                 "active": ["true"],
                                 "algorithm": ["RS256"],
                                 "privateKey": [private_key],
                                 "certificate": [],
                                 "keyUse": ["sig"]}}
        self.keycloak_admin.create_component(component)

        return list(filter(lambda k: k["providerPriority"] == 0, self.keycloak_admin.get_keys()["keys"]))[0]["kid"]

    def get_jwks_uri(self, realm_name):
        return requests.get(self.keycloak_url + "realms/" + realm_name + "/.well-known/openid-configuration").json()["jwks_uri"]
