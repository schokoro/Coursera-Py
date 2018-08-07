import socket

messages = ['ping', 'pong', 'fizz', 'buzz']
host = 'localhost'
port = 10002
timeout = 5

for mess in messages:
    sock = socket.create_connection((host, port), timeout)
    sock.send(mess.encode('utf8'))
    data = sock.recv(1024)
    print(data.decode('utf8'))