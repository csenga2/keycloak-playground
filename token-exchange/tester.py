import requests
import json
import jwt
import pprint

# BEFORE RUNNING
# 1 create confidental client name:test-client
# 2 create a public client name:test-public-client with Direct Access Grants Enabled
# 3 create test user name:test-user/pw:test

keycloak_url = "http://localhost:8080"

client_id = "test-client"
client_secret = "3717d112-6468-41eb-b627-a5e29885384d"

public_client_id = "test-public-client"

user_id = '0a63a838-27b3-496a-84ab-545f0641f65c'
username = 'test-user'
user_password = 'test'


def get_client_token():
    response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token',
                             data={'grant_type': 'client_credentials',
                                   'client_id': client_id,
                                   'client_secret': client_secret})
    return response.json()['access_token']


def get_user_token():
    response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token',
                             data={'grant_type': 'password',
                                   'client_id': public_client_id,
                                   'username': username,
                                   'password': user_password})


    response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token?resource=falcon-user:111',
                             data={'grant_type': 'client_credentials',
                                   'client_id': client_id,
                                   'client_secret': client_secret,
                                   'scope': 'falcon-user-id'})

    return response.json()['access_token']


def token_exchange(data):
    response = requests.post(keycloak_url + '/auth/realms/master/protocol/openid-connect/token',
                             data=data)
    return response.json()['access_token']


def print_decoded_jwt(token, name):
    print('#############################')
    print(name)
    print('#############################')
    pprint.pprint(jwt.decode(token, options={"verify_signature": False}))


if __name__ == '__main__':
    user_token = get_user_token()
    print_decoded_jwt(user_token, 'user_token')

    client_token = get_client_token()
    print_decoded_jwt(client_token, 'client_token')

    # # client can impersonate user
    exchanged_token = token_exchange({'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
                                      'client_id': client_id,
                                      'client_secret': client_secret,
                                      'requested_subject': user_id,
                                      'subject_token': client_token})
    print_decoded_jwt(exchanged_token, 'exchanged_token')

    # client can exchange existing KC token created for a specific client for a new token targeting a new client
    exchanged_token = token_exchange({'grant_type': 'urn:ietf:params:oauth:grant-type:token-exchange',
                                      'client_id': client_id,
                                      'client_secret': client_secret,
                                      'subject_token': user_token})
    print_decoded_jwt(exchanged_token, 'exchanged_token')
