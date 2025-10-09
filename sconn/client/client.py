from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from os.path import exists
from .handlers.client_abstract_handler import ClientAbstractHandler
from .handlers.client_sc_model_handler import ClientSCModelHandler
from ..utils.config_interface import ClientConfig
from ..protocol.constants import ConnectionModels
from ..protocol.transmission import send_packet, recv_packet
from ..protocol.packet_builder import build_packet
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_CLIENT


def tls_wrap_connection(skt: socket, config: ClientConfig) -> SSLSocket:
    tls_context = SSLContext(PROTOCOL_TLS_CLIENT)
    tls_context.load_verify_locations(config.get_ca_certificate_path())
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt, server_hostname=config.get_server_hostname())


class Client:
    def __init__(self, connection_type: ConnectionModels, 
                 config_path: str = "sconn_client_config.yaml") -> None:
        self.config = ClientConfig(config_path)
        
        self.handler: ClientAbstractHandler
        assert connection_type is not ConnectionModels.UNDEFINED_MODEL, "You must choose a defined model."
        self.connection_type = connection_type
        
        
    def connect(self) -> None:
        skt = socket(AF_INET, SOCK_STREAM)
        skt.connect((self.config.get_server_hostname(), 
                     self.config.get_port()))
        skt = tls_wrap_connection(skt, self.config)
        
        model_request = build_packet("001", {"requested-model": str(int(ConnectionModels.SERVER_CLIENT))})
        send_packet(skt, model_request)
        
        server_hello = recv_packet(skt, self.config)
        assert server_hello.code == "051", "Server did not respond to Client Hello with Server Hello."
        
        model_supported = recv_packet(skt, self.config)
        assert model_supported.code == "052", "Server does not support the requested model."
        
        self.assign_specialized_handler(skt)
        
        
    def assign_specialized_handler(self, skt: SSLSocket) -> None:
        match self.connection_type:
            case ConnectionModels.SERVER_CLIENT:
                self.handler = ClientSCModelHandler(skt, self.config)
            case _:
                raise ValueError("The chosen connection model is not supported by the client.")
        

    def disconnect(self) -> None:
        self.handler.socket.shutdown(SHUT_RDWR)
        self.handler.socket.close()
        
    def send(self, data: bytes) -> None:
        self.handler.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        """Receives data from the server connection by using the handler's recv() function.

        :param buffer_len: The maximum amount of bytes to receive at once, defaults to 1024
        :type buffer_len: int, optional
        :param flags: The flags to be passed into the socket.recv() function, defaults to 0
        :type flags: int, optional
        :return: A bytes object that represents the data received.
        :rtype: bytes
        """
        return self.handler.recv(buffer_len, flags)
