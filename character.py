#!/usr/bin/env python3

class Character:
    '''all character relevant data gets stored in here'''
    def __init__(self, width, height, pixels, exp=0,levelcurve=0):
        '''we need all relevant data, everything not mentioned gets reset to default
        arguments:
                width/height = dimensions the sprite image has
                pixels = list of tupels of pixel colors, information about all sprite pixels
                exp = amount of exp the character already gained
                levelcurve = how fast does the character level up?
        '''
        self.width = width
        self.height = height
        self.pixels = pixels
        self.exp = exp
        self.levelcurve = levelcurve
        self.level = self.get_level(self.exp, self.levelcurve)
        self.mexp = self.get_mexp(self.level+1, self.levelcurve)

    def get_width(self):
        '''pixel width'''
        return self.width

    def get_height(self):
        '''pixel height'''
        return self.height

    def get_pixels(self):
        '''list of color tupels, the image is composed of'''
        return self.pixels

    def set_width(self, width):
        '''set new width, as soon as image changes'''
        self.width = width

    def set_height(self, height):
        '''set new height, as soon as image changes'''
        self.height = height

    def get_exp(self):
        '''get current experience'''
        return self.exp
        
    def set_exp(self, exp):
        '''change experience'''
        self.exp = exp
        
    def get_levelcurve(self):
        '''the leveling curve'''
        return self.levelcurve
        
    def get_m_exp(self):
        '''mexp'''
        return self.mexp

    def get_mexp(self, level, curve):
        '''for max exp we need to know the level curve and the level
        arguments:
                level = what's the next level the character wants to reach?
                curve = how fast is he reaching the next level?
        returns:
                exp for next level
        '''
        if curve == 0: # faster
            if level <= 50:
                return int((level**3*(100-level))/50)
            elif level <= 68:
                return int((level**3*(150-level))/100)
            elif level <= 98:
                return int((level**3((1911-10*level)//3))/500)
            else:
                return int((level**3*(160-level))/100)
        elif curve == 1: # slow
            return int((6/5)*(level**3) - 15*(level**2) + 100*level-140)
        else: # really slow
            if level <= 15:
                return int(level**3*((((level+1)//3)+24)/50))
            elif level <= 36:
                return int(level**3*((level+14)/50))
            else:
                return int(level**3*(((level//2)+32)/50))

    def get_level(self, exp, curve):
        '''given exp and level curve we calculate the level
        arguments:
                exp = already made progress
                curve = speed how fast the character grows
        returns:
                level = calculated level
        '''
        level = 0
        mexp = self.get_mexp(level, curve)

        while mexp < exp:
            level += 1
            mexp = self.get_mexp(level+1, curve)

        return level
        
    def get_lvl(self):
        '''returns level'''
        return self.level

    def level_up(self):
        '''after reaching a new level, change level and max exp'''
        self.level += 1
        self.mexp = self.get_mexp(self.level+1, self.levelcurve)
        
if __name__ == '__main__':
    test = Character(0,0,[], 10)
    print(test.get_level(10, 0), test.get_m_exp(), test.get_exp())
