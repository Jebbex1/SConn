from sconn.server.server import Server
from sconn.client.client import Client
from sconn.protocol.constants import ConnectionTypes
from functools import partial
from sconn.protocol.transmission import send_packet
from sconn.protocol.packet_builder import build_packet
import time


def foo(client_socket, config):
    # send_packet(client_socket, build_packet("000"))
    time.sleep(3)

    
s = Server(config_path="testing_server_config.yaml",
           handler_exit_function=partial(foo))
s.start()

time.sleep(3)
s.stop()

"""
Revamped internal logic, added internal protocol to build, transmit, receive, and analyse packets. More in the description

Servers can now support multiple communication models at once.
Deleted usage of server connection handlers and server-side dynamic handler assignment in favour of readability.
Added classes to manage the config interface for both the client and the server.
Migrated default config settings into files instead of string in the code.

"""