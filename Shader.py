from builtins import staticmethod
from OpenGL.GL import *


class Shader:
    @staticmethod
    def readshader(Title, filepath):
        NewFile = ''

        Start = False
        done = False

        if Title == "VERTEX":
            Title = "@VERTEX "
        elif Title == "FRAGMENT":
            Title = "@FRAGMENT "

        with open(filepath, "r") as fp:
            while not done:
                line = fp.readline()
                AFound = False

                if line != "":
                    if line[0] == "@":
                        AFound = True
                        no = False

                        if len(line) == len(Title):
                            for i in range(0, len(Title) - 1):
                                if Title[i] != line[i]:
                                    no = True
                                    break
                        else:
                            no = True
                    if no:
                        Start = False
                    else:
                        Start = True
                else:
                    done = True

                if Start and not done and not AFound:
                    NewFile += line
        return NewFile

    def CreateShader(self, filepath):
        program = glCreateProgram()

        VERT = self.readshader("VERTEX", filepath)
        vertShader = glCreateShader(GL_VERTEX_SHADER)
        self.Compileshader(vertShader, VERT, program, "Vertex")

        FRAG = self.readshader("FRAGMENT", filepath)
        fragShader = glCreateShader(GL_FRAGMENT_SHADER)
        self.Compileshader(fragShader, FRAG, program, "Fragment")

        glLinkProgram(program)
        glValidateProgram(program)
        glDeleteShader(vertShader)
        glDeleteShader(fragShader)

        glUseProgram(program)
        return program

    @staticmethod
    def Compileshader(shader, shaderstring, program, typeos):
        glShaderSource(shader, shaderstring)
        glCompileShader(shader)
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)

        if not status:
            info = glGetShaderInfoLog(shader)
            print("Error in " + typeos + " Shader:")
            print(info.decode("utf-8"))
            glDeleteShader(shader)
        else:
            glAttachShader(program, shader)
