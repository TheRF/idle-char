#!/usr/bin/env python3
from pic import PicShow
import tkinter
from tkinter import *
from cheat_console import CheatWindow
import sys
#from time import sleep

DEBUG=True

class RootWindow(Frame):
    ''''''
    def __init__(self, character, save, zoom, time, master=None, cheats=False):
        ''''''
        tkinter.Frame.__init__(self, master)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.master.title('')
        self.grid()
        
        if DEBUG: print(character, save, zoom, time)
            
        self.create_widgets(character, save, zoom, time, cheats)
        
    def create_widgets(self, character, save, zoom, time, cheats):
        ''''''
        self.chara = PicShow(character, save, master=self, zoom=zoom, time=time)
        self.chara.grid(row=0, column=0)
        if cheats:
            self.cheats = CheatWindow(master=self)
            self.cheats.grid(row=0, column=1)

    def close_window(self):
        '''cleanup routines'''
        self.chara.save_progress()
            
        self.quit()
        
    def inter_communicate(self, data):
        '''allow communication between subwindows'''
        print(data)
        
        self.chara.receive_command(data)
        
    def main_loop(self):
        ''''''
        self.mainloop()
    
