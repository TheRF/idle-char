#!/usr/bin/env python3
import tkinter
from tkinter import *
import os
import os.path
from character import *
from picretrieve import *
from charsav import *

class PicShow(Frame):
    '''main logic of the character'''
    def __init__(self, image, config, master=None, zoom=3, time=900):
        '''load image, savefile and all the other fun stuff
        arguments:
                image = RFG file
                config = save file (car)
                master = root window
                zoom = resize the RFG image
                time = time until auto save (900 = 15 min)
        '''
        # window initialisation
        tkinter.Frame.__init__(self, master)
        if master == None:
            self.master.protocol('WM_DELETE_WINDOW', self.close_window)
            self.master.title('')
        self.grid()
        # logic
        self.picturezoom = zoom
        self.time = time # max time until save
        self.atime = 0
        self.config = config
        self.savefile = ProgToBin()
        if os.path.isfile(config):
            self.exp = self.savefile.convert_from_bin(config)
        else:
            self.exp = 0
        self.get_image_data(image, self.exp)
        self.create_widgets()

#----------------

    def __enter__(self):
        return self

    def __exit__(self):
        self.save_progress()

#----------------

    def get_image_data(self, image, exp):
        '''load the RFG file and zoom the picture
        arguments:
                image = RFG file
                exp = experience from car file
                levelcurve = level speed (savefile, subject to change)
        '''
        rfgfile = RfgConvert()
        rfgfile.read_infos(image)
        levelcurve = rfgfile.get_levelcurve()
        print(levelcurve)
        image_width, image_height = rfgfile.get_dimensions()
        image_width *= self.picturezoom
        image_height *= self.picturezoom
        image_pixels = rfgfile.get_pixels()
        self.chara = Character(image_width, image_height, image_pixels, exp, levelcurve)

#----------------

    def get_zoom_picture(self, image, color, coord, zoom):
        '''we magnify the picture by factor zoom
        arguments:
                image = virtual image
                color = color tupel used for that pixel
                coord = location of this pixel (up left)
        '''
        x, y = coord
        for i in range(0, zoom):
            image.put('#%02x%02x%02x' % color, (x+i,y))
            image.put('#%02x%02x%02x' % color, (x,y+i))
            image.put('#%02x%02x%02x' % color, (x+i,y+i))
            for j in range(0, i):
                image.put('#%02x%02x%02x' % color, (x+i,y+j))
                image.put('#%02x%02x%02x' % color, (x+j,y+i))

#----------------

    def create_widgets(self):
        '''we set all the window elements (image and labels)'''
        # show our picture
        self.img = PhotoImage(width=self.chara.get_width(), height=self.chara.get_height())
        print(len(self.chara.get_pixels()))
        i = 0
        for y in range(0, self.chara.get_height(), self.picturezoom):
            for x in range(0, self.chara.get_width(), self.picturezoom):
                if sum(self.chara.get_pixels()[i]) != 0:
                    self.get_zoom_picture(self.img, self.chara.get_pixels()[i], (x, y), self.picturezoom)
                i += 1
        
        self.pic = tkinter.Label(self, image=self.img)
        self.pic.grid(row=0, column=0)
        self.lvstring = StringVar()
        self.expstring = StringVar()
        #print(self.chara.get_lvl())
        self.lvstring.set('Level: '+str(self.chara.get_lvl()))
        self.expstring.set('Exp: '+str(self.chara.get_exp())+'/'+str(self.chara.mexp))
        print('true: ', self.chara.mexp)
        #print(self.lvstring.get())
        self.lev = tkinter.Label(self, textvariable=self.lvstring)
        self.lev.grid(row=1, column=0)
        self.epoints = tkinter.Label(self, textvariable=self.expstring)
        self.epoints.grid(row=2, column=0)
        
        self.update_stats()

#--------------

    def next_level(self):
        '''get the character on the next level'''
        self.chara.level_up()

#---------------

    def update_stats(self):
        '''add exp, level up, save counter, everything happens here'''
        self.chara.set_exp(self.chara.get_exp()+1)
        #if self.chara.get_exp() >= self.chara.get_mexp(self.chara.get_lvl(), self.chara.get_levelcurve()):
        if self.chara.get_exp() >= self.chara.get_m_exp():    
            self.next_level()
        self.lvstring.set('Level: '+str(self.chara.get_lvl()))
        self.expstring.set('Exp: '+str(self.chara.get_exp())+'/'+str(self.chara.get_m_exp()))
        
        # set the timer, check if we want to save progress
        self.atime += 1
        if self.atime == self.time:
            self.save_progress()
            self.atime = 0
        
        self.after(1000, self.update_stats)

#----------------

    def receive_command(self, data):
        '''get command from parent'''
        if data > 0:
            self.chara.set_exp(self.chara.get_exp()+data)

#----------------

    def close_window(self):
        '''cleanup routine, we close the window using the x button on top'''
        self.save_progress()
        self.quit()
        
    def save_progress(self):
        '''save routine, saves everything into a CAR file'''
        self.savefile.convert_to_bin(self.config, self.chara.get_exp())

    def main_loop(self):
        '''main loop'''
        self.mainloop()

if __name__ == '__main__':
    file='pic.ini'
    pic = PicShow('test.rfg', file, zoom=10)
    pic.main_loop()
