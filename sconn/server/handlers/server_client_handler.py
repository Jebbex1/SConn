from socket import socket
from functools import partial
from .abstract_handler import AbstractHandler


class ServerClientHandler(AbstractHandler):
    def __init__(self, client_socket: socket, exit_function: partial) -> None:
        super().__init__(client_socket)
        self.exit_function = exit_function
        exit_function(handler=self)
    
    
    def send(self, data: bytes) -> None:
        self.client_socket.send(data)
        
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        return self.client_socket.recv(buffer_len, flags)
