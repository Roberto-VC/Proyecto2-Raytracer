import mmap
from os import access
from gl import *

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path) as img:
            m = mmap.mapp(img.fileno(), 0, access=mmap.ACCESS_READ)
            ba = bytearray(m)
            header_size = struct.unpack("=l", ba[10:14][0])
            self.width = struct.unpack("=l", ba[10:14][0])
            self.height = struct.unpack("=l", ba[10:14][0])