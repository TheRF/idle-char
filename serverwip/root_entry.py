#!/usr/bin/env python3
import threading
from root_main import *
import os
import argparse
import configparser
import variables

#-------------------
class ConfigParseError(Exception):
    '''error handling during config file parsing'''
    def __init__(self, message):
        self.message = message

#-------------------
def create_template_config():
    '''create a bsic template configuration file'''
    conf = configparser.ConfigParser()
    conf['FILES'] = { 'character' : variables.character,
                      'save'      : variables.save}
    conf['SERVER']= { 'host'      : variables.host,
                      'port'      : variables.port}
    with open(variables.config, 'w') as configfile:
        conf.write(configfile)
#-------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='server application that lets a character level up on input')
    parser.add_argument('-c', '--config', help='the main configuration file', type=str)
    parser.add_argument('-z', '--zoom', help='size of the shown character', type=int, metavar='INT')
    parser.add_argument('-t', '--time', help='time until autosave', type=int, metavar='INT')
    parser.add_argument('-hs', '--host', help='custom host', type=str, metavar='STR')
    parser.add_argument('-p', '--port', help='custom port number', type=int, metavar='INT')
    parser.add_argument('--noserver', help='run in no server mode', action='store_true')

    args = parser.parse_args()

    # read config file
    # if there's no config, create a new template
    config = variables.config
    if args.config:
        if os.path.isfile(args.config):
            config = args.config
        else:
            raise ConfigParseError('argument: '+args.config+' does not exist; exiting')
    elif not os.path.isfile(variables.config):
            create_template_config()

    cp = configparser.ConfigParser()
    cp.read(config)
    # is it correct? check the sections
    if 'FILES' not in cp or 'SERVER' not in cp:
        raise ConfigParseError('some config sections are missing')
    
    character = ''
    save = ''
    try:
        character = cp['FILES']['character']
        save = cp['FILES']['save']
    except Exception as e:
        raise ConfigParseError('problems during config file parsing: '+e)
    
    # every other argument parsed
    zoom = variables.zoom
    if args.zoom:
        zoom = args.zoom

    time = variables.time
    if args.time:
        time = args.time

    host = cp['SERVER']['host']
    if args.host:
        host = args.host

    port = int(cp['SERVER']['port'])
    if args.port:
        port = args.port

    # now that we finally have everything, we
    # can start the program
    srv = None
    if not args.noserver:
        srv = Server(host, port)
        threading.Thread(target=srv.thread).start()
    root = RootWindow(host, port, character, save, zoom, time, noserver=(args.noserver==True))
    root.main_loop()
    #threading.Thread(target=srv.thread).stop()
    #if not args.noserver:
    #    srv.stop = True