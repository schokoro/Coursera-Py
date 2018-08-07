import asyncio


class ClientServerProtocol(asyncio.Protocol):
    def __init__(self, metrics):
        self.metrics = metrics

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.process_data(data.decode().strip())

    def process_data(self, data):
        mess = data.split()
        if mess[0] == 'put' and len(mess) == 4:
            self.put_data(mess[1:])
        elif mess[0] == 'get' and len(mess) == 2:
            self.get_data(mess[1])
        else:
            self.transport.write('error\nwrong command\n\n'.encode())

    def put_data(self, mess):
        name = mess[0]
        timestamp = int(mess[2])
        value = float(mess[1])
        if name in self.metrics:
            self.metrics[name][timestamp] = value
        else:
            self.metrics[name] = {timestamp : float(mess[1])}
        self.transport.write('ok\n\n'.encode())
        return 'ok\n\n'

    def get_data(self, key):
        preansw = []
        if key == '*':
            for key in self.metrics:
                keyansw = [(key, str(self.metrics[key][timestamp]), str(timestamp)) for timestamp in self.metrics[key]]
                keyansw.sort(key = self.SortByTimeStamp)
                preansw += keyansw
        elif key in self.metrics:
            preansw = [(key, str(self.metrics[key][timestamp]), str(timestamp)) for timestamp in self.metrics[key]]
            preansw.sort(key=self.SortByTimeStamp)

        resp = self.prepare_data(preansw)
        self.transport.write(resp.encode())

    def prepare_data(self, preansw):
        answ = 'ok\n'
        for metric in preansw:
            answ += ' '.join(metric) + '\n'
        answ += '\n'
        return answ

    def SortByTimeStamp(self, metric):
        return metric[2]



def run_server(host, port):
    metrics = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ClientServerProtocol(metrics), host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 10002
    run_server(HOST, PORT)