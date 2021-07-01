'''
Created on Mar 31, 2021

@author: mballance
'''
import json
import sys
import asyncio


class SocketMessageTransport(object):
    
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        
    async def send(self, msg : str):
        header = ("Content-Length: %d\r\n\r\n" % len(msg)).encode()
        self.writer.write(header)
        self.writer.write(msg.encode())
        await self.writer.drain()
        
    async def msgloop(self):
        
        print("==> msgloop")
        while True:
            #********************************************************
            #* Read header
            #********************************************************
            try:
                hdr = await self.reader.read(len("Content-Length: "))
            except ConnectionResetError as e:
                hdr = ""
                print("Disconnect(1)")
                sys.stdout.flush()
                break
            
            if len(hdr) == 0:
                print("Disconnect(2)")
                sys.stdout.flush()
                break
           
            hdr_s = hdr.decode()
            print("hdr=" + hdr_s)
            
            if hdr_s != "Content-Length: ":
                print("Error: unknown header \"%s\"" % hdr_s)
                
            #********************************************************
            #* Read up to first '\n'
            #********************************************************
            size_s = ""
            
            while True:
                c = await self.reader.read(1)
                
                print("c=" + str(c))
                
                if c[0] == 0xa:
                    break
                else:
                    size_s += "%c" % c[0]
                    
            print("size_s=%s" % size_s)
            
            size = int(size_s.strip())
            
            body_s = ""
            
            while len(body_s) < size:
                tmp = await self.reader.read(size-len(body_s))

                #                 
                body_s += tmp.decode().strip()

            print("body=" + body_s + " len=" + str(len(body_s)))
            
            msg = json.loads(body_s)
            
            print("msg=" + str(msg))

        # Halt the event loop
#        asyncio.get_event_loop().stop()            
        print("<== msgloop")
        sys.stdout.flush()
        pass
    