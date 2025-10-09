from yaml import dump, load, safe_load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import sys, os

sys.path.insert(0, "../..")  # add the relative path of the default settings to the path var

SERVER_DEFAULT_CONFIG = open("defualt_server_config.yaml", "r").read()
CLIENT_DEFAULT_CONFIG = open("defualt_client_config.yaml", "r").read()


class BaseConfig:
    def __init__(self, config_file_path: str, server_side: bool):
        if not os.path.exists(config_file_path):
            f = open(config_file_path, "w")
            defualt_config = SERVER_DEFAULT_CONFIG if server_side else CLIENT_DEFAULT_CONFIG
            f.write(defualt_config)
            f.close()
        self.config_yaml = load(open(config_file_path, "r"), Loader=Loader)
        self.config_file_path = config_file_path
    
    def use_mtls(self) -> bool:
        return self.config_yaml["use_mtls"]

    def get_port(self) -> int:
        return self.config_yaml["port"]
    
    def get_recv_buffer_size(self) -> int:
        return self.config_yaml["recv_buffer_size"]


class ServerConfig(BaseConfig):
    def __init__(self, config_file_path: str):
        super().__init__(config_file_path, True)
        
    def get_tls_certificate_paths(self) -> tuple[str, str]:
        return self.config_yaml["certificate_path"], self.config_yaml["certificate_key_path"]

    def get_mtls_ca_certificate_path(self) -> str:
        return self.config_yaml["mtls_trusted_ca_certificate_path"]
    
    def supports_sc_model(self) -> bool:
        return self.config_yaml["supported_models"]["sc_model"]
    
    def supports_rbg_model(self) -> bool:
        return self.config_yaml["supported_models"]["rbg_model"]
    
    def supports_ubg_model(self) -> bool:
        return self.config_yaml["supported_models"]["ubg_model"]

class ClientConfig(BaseConfig):
    def __init__(self, config_file_path: str):
        super().__init__(config_file_path, False)
        
    def get_server_hostname(self) -> str:
        return self.config_yaml["server_hostname"]
    
    def get_ca_certificate_path(self) -> str:
        return self.config_yaml["ca_certificate_path"]
    
    def get_mtls_certificate_path(self) -> str:
        return self.config_yaml["mtls_client_certificate"]
