from socket import socket
from functools import partial
from .server_abstract_handler import ServerAbstractHandler


class ServerSCModelHandler(ServerAbstractHandler):
    def __init__(self, skt: socket, exit_function: partial) -> None:
        super().__init__(skt)
        self.exit_function = exit_function
        exit_function(handler=self)
    
    def send(self, data: bytes) -> None:
        self.socket.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        return self.socket.recv(buffer_len, flags)
