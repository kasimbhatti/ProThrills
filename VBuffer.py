from builtins import staticmethod
from OpenGL.GL import *


class VertexBuffer:
    def __init__(self, vertexSize):
        self.buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, int(12 * (vertexSize/3)), ctypes.c_void_p(24))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, int(12 * (vertexSize/3)), ctypes.c_void_p(0))
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, int(12 * (vertexSize/3)), ctypes.c_void_p(36))
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, int(12 * (vertexSize/3)), ctypes.c_void_p(48))

    @staticmethod
    def AddData(data):
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

    def BindBuffer(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)

    @staticmethod
    def UnBindBuffer():
        glBindBuffer(GL_ARRAY_BUFFER, 0)
