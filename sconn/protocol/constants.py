from enum import IntEnum

class ConnectionTypes(IntEnum):
    """An IntEnum that represents all the connection types.
    """
    UNDEFINED_MODEL      = 0  # used for when a client requests an undefined model
    SERVER_CLIENT        = 1
    OPEN_BROADCAST       = 2
    ROOM_BASED_GROUP     = 3
    USERNAME_BASED_GROUP = 4

SEP = b"\x1d\x0d"  # protocol separator: group separator + carriage return
END = b"\x04"  # end of packet marker
CHARSET = 'utf-8'
LFS = 32

# packet codes
"""
    "CODE": ("DESCRIPTION",
            [
                "header1name",
                "header2name",
            ]),
"""
CODES: dict[str, tuple[str, list[str]]] = {
    # 0xx: Informational, file uploads, predetermined connection model packets
    "000": ("File upload",
            []),
    "001": ("Client Hello",
            [
                "requested-model",
            ]),
    
    "051": ("Server Hello",
            [
                # "length-field-size",
            ]),
    "052": ("Model Supported Transferring",
            []),
    "053": ("Transfer Complete, Initiate Model Handshake",
            []),


    # 1xx: Server-Client Model
    

    # 2xx: Open Broadcast Model


    # 3xx: Room-Based-Groups Model


    # 4xx: User-Based-Groups Model


    # 5xx: Protocol and non-side specific errors (always followed by disconnecting)
    "500": ("Disconnect notification",
            [
                "reason",
            ]),
    "501": ("Transmission protocol error",
            []),
    "502": ("Packet structure error",
            []),
    "503": ("Packet contents error",
            [
                "description",
            ]),
    "504": ("Unsupported Model",
            []),
}