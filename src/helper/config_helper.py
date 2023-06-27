from yaml import dump, safe_load
from os import path
from io import open


"""Finds filepath after compiling."""
def set_file_path():
    bundle_dir = path.dirname(path.abspath(__file__))
    bundle_dir = path.dirname(bundle_dir)
    bundle_dir = path.dirname(bundle_dir)
    return bundle_dir + '\\config\\config.yml'


def save_config(item, value):
    data = read_config()
    data[item] = value
    with open(set_file_path(), 'w', encoding='utf8') as outfile:
        dump(data, outfile, default_flow_style=False, allow_unicode=True)


def read_config():
    with open(set_file_path(), 'r') as outfile:
        config = safe_load(outfile)
    return config

