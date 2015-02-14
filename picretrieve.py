#!/usr/bin/env python3
from crc import CRC

class RFGRetrieveError(Exception):
    '''catches all errors during file parsing'''
    def __init__(self, message):
        self.message = message

class RfgConvert:
    '''read an RFG file, check integrity and get all information
    RFG specs: <0x89>(binary file, 1 byte)<RFG>(file extention, 3 bytes)
               <levelcurve>(leveling speed, 1 byte)
               <palettelength>(number of colors, 2 bytes)
               <palette>(all colors, 3 bytes per color)
               <width><height>(image dimensions, 2 bytes each)
               <pixels>(references to the palette, 1 byte each)
               <crc>(checksum, 1 byte)
    '''
    def __init__(self, crc=CRC()):
        '''we need a crc table
        arguments:
                crc = checksum object
        '''
        self.crc = crc
        # everything else
        self.palette = []
        self.palettelength = 0
        self.pixels = []
        self.width = 0
        self.height = 0
        self.levelcurve = 0

#-----------------

    def intlist_to_int(self, data=[]):
        '''puts a list of integers into one big integer
        arguments:
                data = list of integers < 256
        returns:
                fullnumber = glued together integer
        '''
        print('length: ',len(data))
        if len(data) == 0:
            return 0
        bytes = []
        shift = (len(data)-1) * 8
        for i in data:
            bytes.append(i << shift)
            shift -= 8
        
        fullnumber = 0
        
        for i in bytes:
            fullnumber |= i
            
        return fullnumber

#-----------------

    def read_infos(self, image):
        '''we read the given image and extract all given information
        arguments:
                image = name of the RFG file
        '''
        pic = image

        with open(pic, 'rb') as f:
            # read the whole file and check if correct filetype
            data = []
            g = f
            byte = f.read(1)
            while byte != b'':
                data.append(int.from_bytes(byte, byteorder='big'))
                byte = f.read(1)
                
            if chr(data[1]) != 'R' or chr(data[2]) != 'F' or chr(data[3]) != 'G':
                raise RFGRetrieveError('file is not an RFG file')
                
            # check crc checksum
            crc = self.crc.get_crc(data[:len(data)-1], len(data)-1)
            oldcrc = data[len(data)-1]
            print('crc: ', crc)
            print('old crc: ', oldcrc)
            if crc != oldcrc:
                raise RFGRetrieveError('checksums differ, RFG file corrupt')
            
            # first is the levelcurve
            self.levelcurve = data[4]
            
            palettestart = 7
            # we get palette length and full palette
            self.palettelength = int.from_bytes(data[5:palettestart], byteorder='big')
            index = 0
            start = palettestart
            self.palette = []
            while index < self.palettelength:
                self.palette.append((data[start], data[start+1], data[start+2]))
                index += 1
                start += 3
                
            # now we only need the actual image data
            # dimensions
            start = palettestart + (3*self.palettelength)
            self.width = int.from_bytes(data[start:start+2], byteorder='big')
            start += 2
            self.height = int.from_bytes(data[start:start+2], byteorder='big')
            
            # actual pixels
            # list of indices
            index = 0
            start = palettestart + (3*self.palettelength) + 4
            pixels = []
            while index < self.width*self.height:
                pixels.append(int.from_bytes(data[start:start+2], byteorder='big'))
                index += 1
                start += 2
            #retrieve color from palette
            self.pixels = []
            for i in pixels:
                self.pixels.append(self.palette[i])
            
#-------------------            
                
    def get_dimensions(self):
        '''width and height'''
        return (self.width, self.height)

    def get_palette(self):
        '''the palette'''
        return self.palette

    def get_pixels(self):
        '''the whole image'''
        return self.pixels
        
    def get_levelcurve(self):
        '''the character's levelcurve'''
        return self.levelcurve

if __name__ == '__main__':
    obj = RfgConvert()
    obj.read_infos('stuff.rfg')
    print(obj.get_pixels())
    print(obj.get_levelcurve())
