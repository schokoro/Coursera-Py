import time
import socket
import pdb

class Client:
    def __init__(self, host, port, timeout=None):
        #self.sock = socket.socket()
        #self.sock.connect((host, port))
        self.sock = socket.create_connection((host, port), timeout)
        if not timeout:
            self.sock.settimeout(timeout)

    def put(self, m_name, m_value, timestamp=int(time.time())):
        mess = ' '.join(('put', m_name, str(m_value), str(timestamp))) + '\n'
        #pdb.set_trace()
        answ = self.exchange(mess)
        print(answ)
        if answ != 'ok\n\n':
            raise ClientError

    def get(self, key):
        mess = ' '.join(('get', key)) + '\n'
        answ = self.exchange(mess)
        print(answ)
        if answ.startswith('ok') and answ.endswith('\n\n'):
            return self.get_dict(answ)
        else:
            raise ClientError

    def send(self, key):
        mess = key + '\n'
        answ = self.exchange(mess)
        if answ.endswith('\n\n'):
            return answ
        else:
            raise ClientError

    def exchange(self, mess):
        self.sock.send(mess.encode("utf8"))
        data = b''
        while not data.endswith(b"\n\n"):
            data += self.sock.recv(1024)
        return data.decode("utf8")

    def get_dict(self, answ):
        result = {}
        lines = answ.split('\n')
        for line in lines:
            line = line.split()
            if len(line) != 3:
                continue
            if line[0] in result:
                result[line[0]].append((int(line[2]), float(line[1])))
            else:
                result[line[0]] = [(int(line[2]), float(line[1]))]
        return result


class ClientError(Exception):
    """Socket exception"""
    pass

