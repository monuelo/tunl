import os
import configparser

config = configparser.ConfigParser()

config_path = os.path.dirname(os.path.abspath(__file__)) + '/setup.cfg'

config.read(config_path)

host = config.get('general', 'host')

port = config.get('general', 'port')

debug = config.get('general', 'debug').lower()

kubeconfig = config.get('general', 'kubeconfig')

if debug == "true":
    debug = True
elif debug == "false":
    debug = False
