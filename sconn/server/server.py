from socket import socket, AF_INET, SOCK_STREAM, SHUT_RDWR
from multiprocessing import Process
from threading import Thread
from os.path import exists
from functools import partial
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_SERVER, Purpose, create_default_context
from ..utils.config_interface import ServerConfig
from ..protocol.constants import ConnectionModels
from ..protocol.transmission import recv_packet, send_packet
from ..protocol.packet_builder import build_packet
from ..protocol.communication_errors import PacketContentsError
from ..utils.connection_utils import safe_disconnect


def tls_wrap_client_connection(client_socket: socket, config: ServerConfig) -> SSLSocket:
    if config.use_mtls():
        tls_context = create_default_context(Purpose.CLIENT_AUTH)
        for trusted_ca_cert_path in config.get_trusted_mtls_ca_certificate_paths():
            tls_context.load_verify_locations(trusted_ca_cert_path)
    else:
        tls_context = SSLContext(PROTOCOL_TLS_SERVER)
    certfile_path, keyfile_path = config.get_tls_certificate_paths()
    tls_context.load_cert_chain(certfile=certfile_path, 
                                keyfile =keyfile_path)
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(client_socket, server_side=True)


def get_requested_model(client_socket: SSLSocket, config: ServerConfig) -> ConnectionModels:
    packet = recv_packet(client_socket, config)
    packet.verify_code("001")
    
    try:
        requested_model = int(packet.headers["requested-model"])
    except ValueError as e:
            raise PacketContentsError(f"Packet header types are invalid: {e}")
    
    if requested_model in ConnectionModels:
        return ConnectionModels(requested_model)
    else:
        return ConnectionModels.UNDEFINED_MODEL


def send_unsupported_model(client_socket: SSLSocket) -> None:
    packet = build_packet("504")
    send_packet(client_socket, packet)


class Server:
    def __init__(self, 
                 config_path: str = "sconn_server_config.yaml",
                 handler_exit_function: partial | None = None) -> None:
        """Initializes the Server object, and creates a default config file if the path for it is empty.

        :param connection_type: A ConnectionTypes enum selection, to specify the model of the connection.
        :type connection_type: ConnectionTypes
        :param handler_exit_function: If the handler interacts with the client directly after the initial handshake 
         (e.g. a Server-Client Model), we need to route the process to the function that does that, this parameter is that function. 
         Defaults to None.
        :type handler_exit_function: partial | None, optional
        """

        self.config = ServerConfig(config_path)
            
        self.skt = socket(AF_INET, SOCK_STREAM)
        self.skt.bind(('0.0.0.0', self.config.get_port()))
        
        self.handler_exit_function = handler_exit_function
                
        self.listening_thread = Thread(target=self._start_listening)
        
        if self.config.supports_sc_model():
            assert self.handler_exit_function is not None, "Must define handler exit function if the Server-Client model is supported."
        
        
    def _start_listening(self) -> None:
        """Initiates the listening process of the server, separates each client into a process of its own.
        """
        self.skt.listen()
        try:
            while True:
                client_socket, addr = self.skt.accept()
                client_socket.setblocking(True)
                self.patch_client_to_specialized_handler(client_socket)
        except OSError:  # self.stop() was called
            return


    def patch_client_to_specialized_handler(self, client_socket: socket) -> None:
        client_socket = tls_wrap_client_connection(client_socket, self.config)
        requested_model = get_requested_model(client_socket, self.config)
        send_packet(client_socket, build_packet("051"))  # reply with Server Hello regardless of the model
        match requested_model:
            case ConnectionModels.SERVER_CLIENT if self.config.supports_sc_model():
                send_packet(client_socket, build_packet("052"))
                subprocess = Process(target=self.handler_exit_function, args=(client_socket, self.config))
                subprocess.start()
                return
            case _:
                send_unsupported_model(client_socket)
                safe_disconnect(client_socket)
                return

    
    def start(self) -> None:
        """Starts the listening thread.
        """
        self.listening_thread.start()
    
    
    def stop(self) -> None:
        """Effectively stops the server by closing its listening socket, this interrupts the listening process, and all the client processes.
        """
        safe_disconnect(self.skt)
