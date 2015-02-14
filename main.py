#!/usr/bin/env python3
import argparse
import pic
import os
import configparser

def create_config(config):
    print(config)
    conf = configparser.ConfigParser()
    conf['FILES'] = { 'character' : 'char.rfg',
                        'save' : 'save.car'}
    with open(config, 'w') as configfile:
        conf.write(configfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A character is leveling up.')
    parser.add_argument('config', help='configuration file, that gets to be displayed', type=str)
    parser.add_argument('-m', '--master', help='for embedding it in another window', type=str, metavar='ROOT')
    parser.add_argument('-z', '--zoom', help='zoom size for the shown picture', type=int, metavar='INT')
    parser.add_argument('-t', '--time', help='time until autosave', type=int, metavar='INT')

    args = parser.parse_args()

    master = None
    zoom = 1
    time = 900
    if args.master:
        master = args.master
    if args.zoom:
        if args.zoom > 0:
            zoom = args.zoom
    if args.time:
        if args.time > 0:
            time = args.time
        
    # TODO ini file for character and save file location
    if not os.path.isfile(args.config):
        create_config(args.config)
    
    config = configparser.ConfigParser()
    config.read(args.config)
    char = config['FILES']['character']
    sav = config['FILES']['save']

    window = pic.PicShow(char, sav, master, zoom, time)
    window.main_loop()
