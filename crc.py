#!/usr/bin/env python3
import ctypes

class CRC:
    '''a table driven algorithm to calculate crc checksums'''
    def __init__(self, crcTable=[], poly=0xd8):
        '''set all neccessary information needed to create a
           crc table. after that a simple call for get_crc()
           suffices
        arguments:
                crcTable = is there already a tabe, or do we need
                           to write a new one?
                poly = number that's getting to be used as a divisor
        '''
        self.crcTable = crcTable
        self.POLYNOMIAL = poly
        self.WIDTH = ctypes.sizeof(ctypes.c_uint8) * 8
        self.TOPBIT = (1 << (self.WIDTH - 1))
        if len(self.crcTable) == 0:
            self.create_crc_table()
        elif len(self.crcTable) != 256:
            self.crc = []
            self.create_crc_table()

#----------------

    def create_crc_table(self):
        '''create a crc table that can be used for future
           checksum calculations (division)
        '''
        remainder = ctypes.c_uint8(0)

        for dividend in range(0,256):
            remainder.value = dividend << (self.WIDTH - 8)
            bit = ctypes.c_uint8(8)
            while bit.value > 0:
                if remainder.value & self.TOPBIT:
                    remainder.value = (remainder.value << 1) ^ self.POLYNOMIAL
                else:
                    remainder.value = (remainder.value << 1)
                bit.value -= 1
            self.crcTable.append(remainder.value)

#----------------

    def get_crc(self, message, nBytes):
        '''the actual checksum as the remainder of message and polynom
        arguments:
                message = list of integers (<256)
                nBytes = length of the message
        returns:
                remainder = actual crc checksum
        '''
        data = ctypes.c_uint8(0)
        remainder = ctypes.c_uint8(0)

        for byte in range(0, nBytes):
            data.value = message[byte] ^ (remainder.value >> (self.WIDTH - 8))
            remainder.value = self.crcTable[data.value] ^ (remainder.value << 8)
        return remainder.value

if __name__ == '__main__':
    crc = CRC()
    crc.create_crc_table()
    stre = [0,1,2,3,10]
    print(crc.get_crc(stre, len(stre)))
