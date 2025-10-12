from yaml import dump, load, safe_load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import sys, os

sys.path.insert(0, "../..")  # add the relative path of the default settings to the path var

SERVER_DEFAULT_CONFIG_PATH = "default_server_config.yaml"
CLIENT_DEFAULT_CONFIG_PATH = "default_client_config.yaml"


def get_dict_keys(d: dict) -> list:
    key_list = []
    for k, v in d.items():
        key_list.append(k)
        if isinstance(v, dict):
            key_list.append(get_dict_keys(v))
            
    return key_list


class BaseConfig:
    def __init__(self, config_file_path: str, server_side: bool):
        if not os.path.exists(config_file_path):
            f = open(config_file_path, "w")
            default_config = open(SERVER_DEFAULT_CONFIG_PATH, "r").read() if server_side else open(CLIENT_DEFAULT_CONFIG_PATH, "r").read()
            f.write(default_config)
            f.close()
        self.config_yaml = safe_load(open(config_file_path, "r"))
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
        ServerConfig.validate_server_config_file(self.config_yaml)
        
    def get_tls_certificate_paths(self) -> tuple[str, str]:
        return self.config_yaml["certificate_path"], self.config_yaml["certificate_key_path"]

    def get_trusted_mtls_ca_certificate_paths(self) -> str:
        return self.config_yaml["mtls_trusted_ca_certificate_paths_list"]
    
    def supports_sc_model(self) -> bool:
        return self.config_yaml["supported_models"]["sc_model"]
    
    def supports_rbg_model(self) -> bool:
        return self.config_yaml["supported_models"]["rbg_model"]
    
    def supports_ubg_model(self) -> bool:
        return self.config_yaml["supported_models"]["ubg_model"]
    
    @staticmethod
    def validate_server_config_file(config_dict: dict) -> None:
        server_example_config = safe_load(open(SERVER_DEFAULT_CONFIG_PATH, "r").read())
        assert get_dict_keys(server_example_config) == get_dict_keys(config_dict), \
            "Opened config file that doesn't have all the necessary settings!"

class ClientConfig(BaseConfig):
    def __init__(self, config_file_path: str):
        super().__init__(config_file_path, False)
        ClientConfig.validate_client_config_file(self.config_yaml)
        
    def get_mtls_certificate_paths(self) -> tuple[str, str]:
        return self.config_yaml["mtls_certificate_path"], self.config_yaml["mtls_certificate_key_path"]
        
    def get_server_hostname(self) -> str:
        return self.config_yaml["server_hostname"]
    
    def get_trusted_ca_certificate_paths(self) -> str:
        return self.config_yaml["trusted_ca_certificate_paths_list"]
    
    def get_mtls_certificate_path(self) -> str:
        return self.config_yaml["mtls_client_certificate"]
    
    @staticmethod
    def validate_client_config_file(config_dict: dict) -> None:
        client_example_config = safe_load(open(CLIENT_DEFAULT_CONFIG_PATH, "r").read())
        assert get_dict_keys(client_example_config) == get_dict_keys(config_dict), \
            "Opened config file that doesn't have all the necessary settings!"
