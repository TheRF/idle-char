#!/usr/bin/env python3
from crc import CRC

class SavFileError(Exception):
    '''catches all errors during file parsing'''
    def __init__(self, message):
        self.message = message

class ProgToBin:
    '''create and read from a custom save file
    specs: <0x89>CAR<exp; 4 bytes>
    
    '''
    def __init__(self, csum=CRC()):
        '''we need to get a crc table for checksum calculations
        arguments:
                csum = object for checksum calculations
        '''
        self.csum = csum

#-----------------

    def convert_to_bin(self, file, exp):
        '''we create a save file as a binary file
        arguments:
                file = binary file in which to save the data
                exp = amound of experience gained
        returns:
                crc = calculated checksum
        '''
        calcdata = []
        writedata = []
        with open(file, 'wb') as f:
            # put all information into shape
            calcdata.append(0x89)
            writedata.append(0x89.to_bytes(1, byteorder='big'))
            
            calcdata.append(ord('C'))
            calcdata.append(ord('A'))
            calcdata.append(ord('R'))
            writedata.append('CAR'.encode())
            
            tmp = exp.to_bytes(4, byteorder='big')
            for i in tmp:
                calcdata.append(i)
            writedata.append(tmp)
            
            # get the checksum
            crc = self.csum.get_crc(calcdata, len(calcdata))
            writedata.append(crc.to_bytes(1, byteorder='big'))
            
            # write the file
            for i in writedata:
                f.write(i)
                
            return crc

#------------------

    def convert_from_bin(self, file):
        '''we get the save file, calc the checksum and get the information
        arguments:
                file = input binary save file
        '''
        with open(file, 'rb') as f:
            # first we need to read the file
            data = []
            dat = f.read(1)
            while dat != b'':
                data.append(int.from_bytes(dat, byteorder='big'))
                dat = f.read(1)
            # check if it's a CAR file
            if chr(data[1]) != 'C' or chr(data[2]) != 'A' or chr(data[3]) != 'R':
                raise SavFileError('save file is not a CAR file')
            # then we calculate the checksum and compare it with the one in the file
            crc = self.csum.get_crc(data[:len(data)-1], len(data)-1)
            
            oldcrc = data[len(data)-1]
            
            if crc != oldcrc:
                raise SavFileError('checksums don\'t match: CAR file corrupted')
                
            # all went well, so we parse the information
            exp = int.from_bytes(data[4:8], byteorder='big')
            
            return exp

if __name__ == '__main__':
    test = ProgToBin()
    test.convert_to_bin('testfile', 200467)
    print(test.convert_from_bin('testfile'))
