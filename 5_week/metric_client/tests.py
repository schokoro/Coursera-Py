from client import Client, ClientError
import socket

def exch(host, port, timeout, mess):
    sock = socket.create_connection((host, port), timeout)
    sock.send(mess.encode('utf8'))
    data = sock.recv(1024)
    return data.decode('utf8')


HOST = '127.0.0.1'
PORT = 10002
TIMEOUT = 2

commands = [
    'get test_key',
    'got test_key',
    'put test_key 12.0 1503319740',
    'put test_key 13.0 1503319739',
    'put test_key 13.0 1503319739',
    'get test_key',
    'put another_key 10 1503319739',
    'get *',
]


for command in commands:
    resp = exch(HOST, PORT, TIMEOUT, command)
    print(command)
    print(resp)
    input()