import yaml
import sys
import os
import io


"""Finds filepath after compiling."""
def set_file_path():
    if getattr(sys, 'frozen', False):  # we are running in a bundle
        bundle_dir = sys._MEIPASS  # This is where the files are unpacked to
    else:  # normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        bundle_dir = os.path.dirname(bundle_dir)
        bundle_dir = os.path.dirname(bundle_dir)
    return bundle_dir + '\\config\\config.yaml'

def save_config(item, value):
    data = read_config()
    data[item] = value
    with io.open(set_file_path(), 'w', encoding='utf8') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)


def read_config():
    with open(set_file_path(), 'r') as outfile:
        config = yaml.safe_load(outfile)
    return config

