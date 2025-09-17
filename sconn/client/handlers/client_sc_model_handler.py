from socket import socket
from .client_abstract_handler import ClientAbstractHandler


class ClientSCModelHandler(ClientAbstractHandler):
    def __init__(self, skt: socket) -> None:
        super().__init__(skt)
    
    def send(self, data: bytes) -> None:
        self.socket.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        return self.socket.recv(buffer_len, flags)