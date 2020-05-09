from builtins import staticmethod
from OpenGL.GL import *


class IndexBuffer:
    def __init__(self):
        self.buffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer)

    @staticmethod
    def AddData(data):
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, data, GL_STATIC_DRAW)

    def BindBuffer(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.buffer)

    @staticmethod
    def UnBindBuffer():
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
