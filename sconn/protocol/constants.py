from enum import IntEnum


# Fixed Protocol Settings (packet structure)
SEP = b"\x1d\x0d"  # protocol separator: group separator + carriage return
END = b"\x04"      # end of packet marker

# Customizable Protocol Settings (defined in config files of the server)
DEFAULT_SETTINGS = {
    "port": 8374,
    "charset": 'utf-8', 
    "length_field_header": 32,   # length header size in bits (default of 4 bytes)
    "max_field_size": 128,   # 128 bytes, which is 182 characters in UTF-8
    "max_title_size": 128,   # 128 bytes, which is 182 characters in UTF-8
    "max_file_size": int(1.6e7), # 16MB
}

class ConnectionTypes(IntEnum):
    SERVER_CLIENT   = 1
    CLIENT_CLIENT   = 2
    OPEN_BROADCAST  = 3
    BROADCAST_GROUP = 4