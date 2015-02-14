#!/usr/bin/env python3

from PIL import Image

class PictureInfo:
    '''we retrieve all the needed information from the image'''
    def __init__(self):
        pass

#-------------------

    def load_image(self, image):
        '''we get the image and convert it to get access to the palette
        arguments:
                image = name and location of the original image
        '''
        # FIXME needs a conversion algorithm that optimizes the palette
        # right now works best with an already indexed picture
        try:
            pic = Image.open(image)
            self.pic = pic.convert('RGB')
        except Exception:
            print('image could not be loaded')
            exit(1)

#-------------------

    def get_dimensions(self):
        '''width and height'''
        return self.pic.size

#-------------------

    def get_palette(self):
        '''lookup every pixel and check if we already found this color
        returns:
                palette, colors = finished palette and unindexed picture
        '''
        # get pixels from image
        x, y = self.get_dimensions()
        colors = []
        for j in range(0, y):
            for i in range(0, x):
                colors.append(self.pic.getpixel((i, j)))
        # get palette from pixels
        palette = []
        for i in colors:
            if i not in palette:
                palette.append(i)

        return (palette, colors)

#------------------

    def get_color_index(self):
        '''take the colors and reduce them to the index in the palette
        returns:
                index = list of indiced pixels
        '''
        palette, colors = self.get_palette()
        index = []
        for i in colors:
            j = 0
            while j < len(palette):
                if i == palette[j]:
                    index.append(j)
                j += 1
                
        return index


if __name__ == '__main__':
    file = 'cel.png'
    info = PictureInfo()
    info.load_image(file)
    print(info.get_color_index())
