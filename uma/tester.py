import requests
import json

keycloak_url = "http://localhost:8080"

client_id = "uma-test"
client_secret = "c7bc930d-5aa8-4915-a161-84d9f43a6f7b"


def print_uma2_configuration():
    r = requests.get(keycloak_url + '/auth/realms/master/.well-known/uma2-configuration')
    print(json.dumps(json.loads(r.text), indent=3))


def get_client_token():
    response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token',
                             data={'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'})
    return response.json()['access_token']


def print_resources(access_token):
    response = requests.get(keycloak_url + '/auth/realms/master/authz/protection/resource_set',
                            headers={'Authorization': 'Bearer ' + access_token})
    print(response.json())


def print_resource(access_token, resource_id):
    response = requests.get(keycloak_url + '/auth/realms/master/authz/protection/resource_set/' + resource_id,
                            headers={'Authorization': 'Bearer ' + access_token})
    print(response.json())


def create_resource(access_token, resource):
    response = requests.post(keycloak_url + '/auth/realms/master/authz/protection/resource_set',
                             json=resource,
                             headers={'Authorization': 'Bearer ' + access_token})
    print(response.json())


if __name__ == '__main__':
    client_token = get_client_token()
    create_resource(client_token, {'name':'test-resource-2','ownerManagedAccess': True, 'type':'test-type'})
    print_resources(client_token)
    print_resource(client_token, 'a58e2531-a516-4821-ad63-4c92a001ff4d')
