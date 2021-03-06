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
    with open(variables.config, 'w') as configfile:
        conf.write(configfile)
#-------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='server application that lets a character level up on input')
    parser.add_argument('-c', '--config', help='the main configuration file', type=str)
    parser.add_argument('-z', '--zoom', help='size of the shown character', type=int, metavar='INT')
    parser.add_argument('-t', '--time', help='time until autosave', type=int, metavar='INT')
    parser.add_argument('--cheat', help='open cheat console')

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
    if 'FILES' not in cp:
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

    # now that we finally have everything, we
    # can start the program

    root = RootWindow(character, save, zoom, time, cheats=args.cheat)
    root.main_loop()
