from keycloak import KeycloakAdmin
from service_account_helper import *
from realm_helper import *

keycloak_url = "http://localhost:8080/"
keycloak_admin = KeycloakAdmin(server_url=keycloak_url,
                               username="admin",
                               password="admin",
                               auto_refresh_token=['get', 'put', 'post', 'delete'])
local_realm_name = "local"
remote_realm_name = "remote"


def main():
    realm_helper = RealmHelper(keycloak_admin, keycloak_url)
    realm_helper.create_realm(local_realm_name)
    keycloak_admin.realm_name = local_realm_name

    service_account = ServiceAccountHelper(keycloak_admin, keycloak_url)

    # service account with client secret
    service_account.test_service_account_with_client_secret(local_realm_name)

    # service account with signed jwt/rsa key
    service_account.test_service_account_with_signed_jwt_provided_by_predefined_rsa_key(local_realm_name)

    # service account with signed jwt/jwks url
    # first a remote realm is created which provides the jwks url, then the client is created
    realm_helper.create_realm(remote_realm_name)
    keycloak_admin.realm_name = remote_realm_name
    kid = realm_helper.add_rsa_key(remote_realm_name)
    remote_realm_jwks = realm_helper.get_jwks_uri(remote_realm_name)

    keycloak_admin.realm_name = local_realm_name
    service_account.test_service_account_with_signed_jwt_by_jwks_url(local_realm_name, remote_realm_jwks, kid)

if __name__ == '__main__':
    main()
