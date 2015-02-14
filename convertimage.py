#!/usr/bin/env python3
import getpictureinfo as gpi
import os
from crc import CRC

class PicToBin:
    '''read a png image file, get all mandatory information out of it
       and create a new RFG file
    RFG specs: <0x89>(binary file, 1 byte)<FG>(file extention, 3 bytes)
               <palettelength>(number of colors, 2 bytes)
               <palette>(all colors, 3 bytes per color)
               <width><height>(image dimensions, 2 bytes each)
               <pixels>(references to the palette, 1 byte each)
               <crc>(checksum, 1 byte)
    '''
    def __init__(self, crc=CRC()):
        '''we need a crc table, so we create one
        arguments:
                crc = checksum object
        '''
        self.crc = crc

#------------------------

    def convert_file_to_bin(self, infile, levelcurve, outfile='default.rfg'):
        '''we get all the information of the image file and put it into an RFG file
        arguments:
                infile = image name
                levelcurve = leveling speed
                outfile = target RFG file
        '''
        # get image data
        if not os.path.isfile(infile):
            raise FileNotFoundError('There\'s no such image called: '+infile)
        info = gpi.PictureInfo()
        info.load_image(infile)
        pal = info.get_palette()[0]
        col = info.get_color_index()
        w, h= info.get_dimensions()
        # write it into new file
        crc = self.write_bin_file(pal, col, w, h, levelcurve, outfile)
        print('File creation completed.')
        print('crc checksum: ', crc)
        return crc

#---------------------

    def convert_palette(self, palette):
        '''convert every color tupel into one big number #rrggbb
        arguments:
                palette = list of color tupels (rr, gg, bb)
        returns:
                list of #rrggbb numbers
        '''
        bytes = []
        for i in palette:
            #print(hex(i[0]), hex(i[1]), hex(i[2]))
            r = i[0] << 16
            g = i[1] << 8
            b = i[2]
            #print(hex(r), hex(g), hex(b))
            bit = 0 | r
            bit = bit | g
            bit = bit | b
            bytes.append(bit)
        return bytes

#------------------------

    def write_bin_file(self, palette, colors, width, height, levelcurve, outfile='default.rfg'):
        '''bring image information into new file format
        arguments:
                palette = list of color tuples used in the image
                colors = list of indices corresponding to the index of the palette
                width/height = dimensions of the image
                levelcurve = leveling speed
                outfile = file where information is getting stored
        returns:
                crc = checksum of all the data
        '''
        with open(outfile, 'wb') as bwriter:
            # first we calculate the checksum
            data = [0x89, ord('R'), ord('F'), ord('G'), levelcurve]
            
            le = len(palette).to_bytes(2, byteorder='big')
            for i in le:
                data.append(i)
            
            for i in palette:
                for j in i:
                    data.append(j)
                    
            w = width.to_bytes(2, byteorder='big')
            for i in w:
                data.append(i)
            h = height.to_bytes(2, byteorder='big')
            for i in h:
                data.append(i)
                
            for i in colors:
                j = i.to_bytes(2, byteorder='big')
                for k in j:
                    data.append(k)
            print(data)
            crc = self.crc.get_crc(data, len(data))
            # then we write the binary file
            bwriter.write(0x89.to_bytes(1, byteorder='big'))
            bwriter.write('RFG'.encode())
            bwriter.write(levelcurve.to_bytes(1, byteorder='big'))
            #print(len(palette))
            bwriter.write(len(palette).to_bytes(2, byteorder='big'))
            for i in self.convert_palette(palette):
                bwriter.write(i.to_bytes(3, byteorder='big'))
            bwriter.write(width.to_bytes(2, byteorder='big'))
            bwriter.write(height.to_bytes(2, byteorder='big'))
            for i in colors:
                bwriter.write(i.to_bytes(2, byteorder='big'))
            # finally we append the checksum
            bwriter.write(crc.to_bytes(1, byteorder='big'))
            
            return crc

if __name__ == '__main__':
    file = 'cel.png'
    
    tobin = PicToBin()
    tobin.convert_file_to_bin(file, 0, outfile='stuff.rfg')
    #tobin = PicToBin([],[],0)
    #tobin.convert_palette([(0, 234, 17)])