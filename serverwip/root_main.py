#!/usr/bin/env python3
from pic import PicShow
import tkinter
from tkinter import *
import select
import socket
import sys
import queue
import threading
#from time import sleep

DEBUG=True

class RootWindow(Frame):
    ''''''
    def __init__(self, host, port, character, save, zoom, time, master=None, noserver=False):
        ''''''
        tkinter.Frame.__init__(self, master)
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.master.title('')
        self.grid()
        
        if DEBUG: print(host, port, character, save, zoom, time, noserver)
        
        self.noserver = noserver
        if not self.noserver:
            # client
            self.create_client(host, port)
            
        self.create_widgets(character, save, zoom, time)
        
        if not self.noserver:
            self.receive_handler()
        
    def create_widgets(self, character, save, zoom, time):
        ''''''
        self.chara = PicShow(character, save, master=self, zoom=zoom, time=time)
        self.chara.grid()
        
    def create_client(self, host, port):
        ''''''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.setblocking(0)
        self.sock.send('imyourking'.encode())

    def receive_handler(self):
        '''listen for a message from our server'''
        data = self.sock.recv(1024).decode()
        if DEBUG: print('receive handler')
        if data:
            if DEBUG: print('receive handler: ',data)
            if data == '':
                # 
                pass
        self.after(1000, self.receive_handler)

    def close_window(self):
        '''cleanup routines'''
        self.chara.save_progress()
        if not self.noserver:
            # get resources free again
            self.sock.send('dieforme'.encode())
            self.sock.shutdown(1)
            
        self.quit()
        
    def main_loop(self):
        ''''''
        self.mainloop()
    
class Server:
    ''''''
    def __init__(self, host, port):
        ''''''
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)
        self.bind(host, port)
        self.listen()
        
        self.stop = False
        
    def bind(self, host, port):
        ''''''
        self.server_address = (host, port)
        print('starting up on %s port %s' % self.server_address, file=sys.stderr)
        self.server.bind(self.server_address)
        
    def listen(self, num=5):
        ''''''
        self.server.listen(num)
        
    def thread(self):
        ''''''
        inputs = [self.server]

        outputs = []

        message_queues = {}
        
        king = None

        #-------------------------------------
        while inputs and not self.stop:
            print('\nwaiting for the next event', file=sys.stderr)
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            # handle inputs
            for s in readable:
                if s is self.server:
                    # a readable server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print('new connection from', client_address, file=sys.stderr)
                    connection.setblocking(0)
                    inputs.append(connection)

                    # give the connection a queue for data we want to send
                    message_queues[connection] = queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        # a readable client socket has data
                        print('received "%s" from %s' % (data, s.getpeername()), file=sys.stderr)
                        if data.decode() == 'imyourking' and not king:
                            king = s
                            print('we found our king', file=sys.stderr)
                            
                        if data.decode() == 'dieforme' and s is king:
                            message_queues[s].put('asyouwishmylord'.encode())
                            if s not in outputs:
                                outputs.append(s)
                        else:
                            message_queues[s].put(data)
                        # add output channel for response
                        if s not in outputs:
                            outputs.append(s)
                    elif s is not king:
                        # interpret empty result as closed connection
                        print('closing', client_address, 'after reading no data', file=sys.stderr)
                        # stop listening for input on the connection
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        s.close()

                        # remove message queue
                        del message_queues[s]

            # handle outputs
            for s in writable:
                try:
                    if DEBUG and s is king: print('main client response')
                    next_msg = message_queues[s].get_nowait()
                    if next_msg == b'asyouwishmylord':
                        if DEBUG: print('ending signal received', file=sys.stderr)
                        self.stop = True
                except queue.Empty:
                    # no message waiting so stop checking for writability
                    print('output queue for', s.getpeername(), 'is empty', file=sys.stderr)
                    outputs.remove(s)
                else:
                    print('sending "%s" to "%s"' % (next_msg, s.getpeername()), file=sys.stderr)
                    s.send(next_msg)

            # handle exceptional conditions
            for s in exceptional:
                print('handling exceptional condition for', s.getpeername(), file=sys.stderr)
                # stop listening for input on the connection
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

                # remove message queue
                del message_queues[s]
