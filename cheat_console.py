#!/usr/bin/env python3
import tkinter
from tkinter import *
import re

class CheatError(Exception):
    ''''''
    pass

class CheatWindow(Frame):
    ''''''
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.grid()
        
        self.create_widgets()
        
    def create_widgets(self):
        ''''''
        self.cheat_textbox = tkinter.Text(self, width=20, height= 1)
        self.cheat_textbox.grid()
        self.send_button = tkinter.Button(self, text='Send', command=self.send_command)
        self.send_button.grid()
        
    def send_command(self):
        '''get text from textbox and send it to root'''
        data = self.cheat_textbox.get("1.0", END).strip('\n')
        if re.fullmatch(r'\d+', data):
            self.master.inter_communicate(int(data))
        self.cheat_textbox.delete(1.0, END)
        
if __name__ == '__main__':
    w = CheatWindow()
    w.mainloop()
