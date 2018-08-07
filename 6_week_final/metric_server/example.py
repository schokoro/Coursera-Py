import asyncio
import logging

def start(self):
    class OPCUAProtocol(asyncio.Protocol):

        """
        instanciated for every connection
        defined as internal class since it needs access
        to the internal server object
        FIXME: find another solution
        """

        iserver = self.iserver
        loop = self.loop

        def connection_made(self, transport):
            self.peername = transport.get_extra_info('peername')
            print('New connection from {}'.format(self.peername))
            self.transport = transport
            self.processor = UAProcessor(self.iserver, self.transport)
            self.data = b""

        def connection_lost(self, ex):
            print('Lost connection from ', self.peername, ex)
            self.transport.close()
            self.processor.close()

        def data_received(self, data):
            logging.debug("received %s bytes from socket", len(data))
            if self.data:
                data = self.data + data
                self.data = b""
            self._process_data(data)

        def _process_data(self, data):
            while True:
                try:
                    buf = ua.utils.Buffer(data[:])
                    hdr = ua.Header.from_string(buf)
                    if len(buf) < hdr.body_size:
                        logging.warning("We did not receive enough data from server, waiting for more")
                        self.data = data
                        return
                    ret = self.processor.process(hdr, buf)
                    if not ret:
                        logging.warning("processor returned False, we close connection")
                        self.transport.close()
                        return
                    if len(data) <= hdr.packet_size:
                        return
                    data = data[hdr.packet_size:]
                except ua.utils.NotEnoughData:
                    logging.warning("Not a complete packet in data from client, waiting for more data")
                    self.data = buf.data
                    break
                except Exception:
                    logging.exception("Exception raised while parsing message from client, closing")
                    self.transport.close()
                    break

    logging.warning("Listening on %s:%s", self.hostname, self.port)
    coro = self.loop.create_server(OPCUAProtocol, self.hostname, self.port)
    self._server = self.loop.run_coro_and_wait(coro)
    logging.warning('Listening on %s', self._server.sockets[0].getsockname())