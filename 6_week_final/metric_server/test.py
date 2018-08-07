import unittest
from client import Client, ClientError
import courserver

HOST = 'localhost'
PORT = 10002
courserver.run_server(HOST, PORT)

