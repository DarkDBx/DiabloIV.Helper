from yaml import dump, safe_load
from os import path
from io import open

def get_file_path():
    """
    Determines the absolute path to the configuration file.
    Assumes the file is located three directories above the script's location in a 'config' folder.
    """
    base_dir = path.abspath(path.join(path.dirname(__file__), '..', '..'))
    return path.join(base_dir, 'config', 'config.yml')

def read_config():
    """
    Reads the configuration from the YAML file.
    Returns the configuration as a dictionary.
    """
    config_path = get_file_path()
    if not path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")
    with open(config_path, 'r', encoding='utf8') as infile:
        return safe_load(infile) or {}

def save_config(item, value):
    """
    Updates the configuration file with a new key-value pair or updates an existing one.
    """
    config_path = get_file_path()
    data = read_config()
    data[item] = value
    with open(config_path, 'w', encoding='utf8') as outfile:
        dump(data, outfile, default_flow_style=False, allow_unicode=True)
