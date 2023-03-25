import yaml
import sys
import os


"""Finds filepath after compiling."""
def set_file_path():
    if getattr(sys, 'frozen', False):  # we are running in a bundle
        bundle_dir = sys._MEIPASS  # This is where the files are unpacked to
    else:  # normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        bundle_dir = os.path.dirname(bundle_dir)
        bundle_dir = os.path.dirname(bundle_dir)
    return bundle_dir + '\\config\\config.yaml'

config_path = set_file_path()

"""
def save_config(var_dict):
    with open(config_path, 'r') as configfile:
        config = yaml.safe_load(configfile)
    var = config.update(var_dict)
    with open(config_path, 'w') as configfile:
        yaml.dump(var, configfile)
"""

def read_config():
    with open(config_path, 'r') as configfile:
        config = yaml.safe_load(configfile)
    return config

