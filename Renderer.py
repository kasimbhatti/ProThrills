from builtins import staticmethod
from OpenGL.GL import *
import numpy
from PIL import Image
import math
from Shader import Shader
from VBuffer import VertexBuffer
from IndexBuffer import IndexBuffer
from os import listdir
from os.path import isfile, join


class Renderer:
    def __init__(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vertexSize = 15
        self.NewBuffer = VertexBuffer(self.vertexSize)
        self.buffer = self.NewBuffer.buffer
        self.NewIndex = IndexBuffer()
        self.ibo = self.NewIndex.buffer
        self.NewShader = Shader()
        self.program = ctypes.c_uint
        self.Identity4 = numpy.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype='float32')

    def returnVertexSize(self):
        return self.vertexSize

    def attachTextures(self, Folder):
        files = [f for f in listdir(Folder) if isfile(join(Folder, f))]
        for i in range(0, len(files)):
            self.AttachTexture(Folder + "\\" + files[i], i, True)
        self.AttachTexture("", len(files), False)
        return len(files) + 1

    def AttachTexture(self, filepath, value, Yes):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, value)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        if Yes:
            TextureA = Image.open(filepath).transpose(Image.FLIP_TOP_BOTTOM)
            TextureString = numpy.frombuffer(TextureA.tobytes(), numpy.uint8)
            Width, Height = TextureA.size
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, Width, Height, 0, GL_RGBA, GL_UNSIGNED_BYTE, TextureString)
        else:
            Empty = Image.new('RGB', (1200, 1200), (255, 255, 255))
            Empty.save("Empty.png", "PNG")
            EmptyString = numpy.frombuffer(Empty.tobytes(), numpy.uint8)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 600, 600, 0, GL_RGBA, GL_UNSIGNED_BYTE, EmptyString)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, int(12 * (self.vertexSize / 3)), ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glActiveTexture(GL_TEXTURE0 + value)
        location = glGetUniformLocation(self.program, "u_Texture")
        glUniform1i(location, value)

    @staticmethod
    def UseTexture(ID):
        glBindTexture(GL_TEXTURE_2D, ID)

    @staticmethod
    def Identity4():
        M = numpy.array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], dtype='float32')
        return M

    @staticmethod
    def Orthographic(l, r, b, t, f, n):
        OMatrix = numpy.array(
            [2 / (r - l), 0, 0, 0,
             0, 2 / (t - b), 0, 0,
             0, 0, 2 / (n - f), 0,
             (r + l) / (l - r), (t + b) / (b - t), (f + n) / (n - f), 1],
            dtype='float32')
        return OMatrix

    def ProjectAndStretch(self, FOVradians, Near, Far, Scale, ScaledRatio):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.3, 0.3, 0.3, 1.0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        Projection = numpy.array(
            [1 / math.tan(FOVradians / 2), 0, 0, 0,
             0, 1 / math.tan(FOVradians / 2), 0, 0,
             0, 0, -Far / (Far - Near), -(Far * Near) / (Far - Near),
             0, 0, -1, 0],
            dtype='float32')
        Stretch = numpy.array([Scale, 0, 0, 0,
                               0, ScaledRatio, 0, 0,
                               0, 0, 1, 0,
                               0, 0, 0, 1],
                              dtype='float32')
        self.SendMat4("u_MVP", Projection)
        self.SendMat4("u_Stretch", Stretch)

    def Rotate(self, a, b, y):
        OXYZ = numpy.array([math.cos(b) * math.cos(y), - math.sin(y) * math.cos(b), math.sin(b),
                            (math.sin(a) * math.sin(b) * math.cos(y)) + (math.sin(y) * math.cos(a)),
                            (-math.sin(a) * math.sin(b) * math.sin(y)) + (math.cos(a) * math.cos(y)),
                            -math.sin(a) * math.cos(b),
                            (-math.sin(b) * math.cos(a) * math.cos(y)) + (math.sin(a) * math.sin(y)),
                            (math.sin(b) * math.cos(a) * math.sin(y)) + (math.sin(a) * math.cos(y)),
                            math.cos(a) * math.cos(b)], dtype='float32')
        self.SendMat3("u_Rotation", OXYZ)

    def RotateQuaternion(self, Quat):
        self.SendVec4("u_Quat", Quat)

    def Translate(self, TX, TY, TZ):
        Translation = numpy.array([TX, TY, TZ], dtype='float32')
        self.SendVec3("u_Translation", Translation)

    def Lighting(self, x, y, z):
        Position = numpy.array([x, y, z], dtype='float32')
        self.SendVec3("lightPos", Position)

    @staticmethod
    def Normal(A, B, C):
        b = [B[0] - A[0], B[1] - A[1], B[2] - A[2]]
        c = [C[0] - A[0], C[1] - A[1], C[2] - A[2]]
        Normal = [b[1] * c[2] - b[2] * c[1], b[2] * c[0] - b[0] * c[2], b[0] * c[1] - b[1] * c[0]]
        NormalLength = math.sqrt(Normal[0] * Normal[0] + Normal[1] * Normal[1] + Normal[2] * Normal[2])
        UnitNormalNumpy = numpy.array([Normal[0] / NormalLength, Normal[1] / NormalLength, Normal[2] / NormalLength],
                                      dtype='float32')
        return UnitNormalNumpy

    def Send(self, Uniform, r, g, b):
        location = glGetUniformLocation(self.program, Uniform)
        glUniform4f(location, r, g, b, 1.0)

    def SendMat4(self, Uniform, SendMatrix):
        location = glGetUniformLocation(self.program, Uniform)
        glUniformMatrix4fv(location, 1, GL_FALSE, SendMatrix)

    def SendMat3(self, Uniform, SendMatrix):
        location = glGetUniformLocation(self.program, Uniform)
        glUniformMatrix3fv(location, 1, GL_FALSE, SendMatrix)

    def SendVec3(self, Uniform, NewVector):
        location = glGetUniformLocation(self.program, Uniform)
        glUniform3fv(location, 1, NewVector)

    def SendVec4(self, Uniform, NewVector):
        location = glGetUniformLocation(self.program, Uniform)
        glUniform4fv(location, 1, NewVector)

    def SendFloat(self, Uniform, NewFloat):
        location = glGetUniformLocation(self.program, Uniform)
        glUniform1f(location, NewFloat)

    def AddShader(self, filepath):
        self.program = self.NewShader.CreateShader(filepath)

    @staticmethod
    def Unbind():
        glBindVertexArray(0)
        glUseProgram(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    def Bind(self):
        glBindVertexArray(self.vao)
        glUseProgram(self.program)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)

    @staticmethod
    def DrawElements(length, offset):
        glDrawElements(GL_TRIANGLES, length, GL_UNSIGNED_INT, ctypes.c_void_p(offset))

    @staticmethod
    def DrawRangeElements(start, end):
        length = (end - start) + 1
        glDrawRangeElements(GL_TRIANGLES, start, end, length, GL_UNSIGNED_INT, None)

    def Draw3D(self, vertices):
        positions = vertices[0]
        faceindices = vertices[2]
        compact = vertices[5]
        self.NewBuffer.AddData(positions)
        self.NewIndex.AddData(faceindices)
        self.NewIndex.BindBuffer()
        offset = 0
        for i in range(0, len(compact)):
            self.UseTexture(i)
            self.DrawElements(int(3 * compact[i]), int(offset * 4))
            offset += int(3 * compact[i])

