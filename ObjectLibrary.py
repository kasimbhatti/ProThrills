import numpy
import math

class ObjectLibrary:
    def __init__(self, textureNumber, vertexSize):
        self.VerticesList = [numpy.array([], dtype='float32'), numpy.array([], dtype='int32'), [], []]
        self.IndicesList = numpy.array([], dtype='int32')
        self.SortedIndicesList = numpy.array([], dtype='int32')
        self.TextureList = []
        self.SortedTextureList = []
        self.CompactTextureList = []
        self.vertexSize = vertexSize
        self.textureNumber = textureNumber

    def returnVertices(self):
        Result = [self.VerticesList, self.IndicesList, self.SortedIndicesList, self.TextureList, self.SortedTextureList, self.CompactTextureList]
        return Result

    def returnVertexSize(self):
        return self.vertexSize

    def removeVertices(self, a):
        offset = a[0]
        offsetEnd = a[1]
        indexOffset = a[2]
        indexOffsetEnd = a[3]
        textureOffset = a[4]
        textureOffsetEnd = a[5]
        self.VerticesList = numpy.delete(self.VerticesList, range(offset, offsetEnd))
        self.IndicesList = numpy.delete(self.IndicesList, range(indexOffset, indexOffsetEnd))
        self.VerticesList = self.VerticesList.astype('float32')
        self.IndicesList = self.IndicesList.astype('int32')
        del self.TextureList[textureOffset:textureOffsetEnd:1]
        self.sortVertices()

    def sortIndexBuffer(self):
        n = len(self.SortedIndicesList)
        for i in range(1, n, 3):
            textureValue = int((i - 1) / 3)

            temp1 = self.SortedIndicesList[i - 1]
            temp2 = self.SortedIndicesList[i]
            temp3 = self.SortedIndicesList[i + 1]
            temp = self.SortedTextureList[textureValue]

            z = textureValue
            z1 = i - 1
            z2 = i
            z3 = i + 1
            while z > 0 and self.SortedTextureList[z - 1] > temp:
                self.SortedTextureList[z] = self.SortedTextureList[z - 1]
                self.SortedIndicesList[z1] = self.SortedIndicesList[z1 - 3]
                self.SortedIndicesList[z2] = self.SortedIndicesList[z2 - 3]
                self.SortedIndicesList[z3] = self.SortedIndicesList[z3 - 3]
                z = z - 1
                z1 = z1 - 3
                z2 = z2 - 3
                z3 = z3 - 3
            self.SortedTextureList[z] = temp
            self.SortedIndicesList[z1] = temp1
            self.SortedIndicesList[z2] = temp2
            self.SortedIndicesList[z3] = temp3

    def partition(self, low, high):
        i = low - 1
        pivot = self.SortedTextureList[high]

        for j in range(low, high):
            if self.SortedTextureList[j] <= pivot:
                i += 1
                self.SortedTextureList[i], self.SortedTextureList[j] = self.SortedTextureList[j], self.SortedTextureList[i]

                self.SortedIndicesList[3 * i], self.SortedIndicesList[3 * j] = self.SortedIndicesList[3 * j], self.SortedIndicesList[3 * i]
                self.SortedIndicesList[3 * i + 1], self.SortedIndicesList[3 * j + 1] = self.SortedIndicesList[3 * j + 1], self.SortedIndicesList[3 * i + 1]
                self.SortedIndicesList[3 * i + 2], self.SortedIndicesList[3 * j + 2] = self.SortedIndicesList[3 * j + 2], self.SortedIndicesList[3 * i + 2]

        self.SortedTextureList[i + 1], self.SortedTextureList[high] = self.SortedTextureList[high], self.SortedTextureList[i + 1]
        return i + 1

    def quickSortIndexBuffer(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quickSortIndexBuffer(low, pi - 1)
            self.quickSortIndexBuffer(pi + 1, high)

    def compactSortedIndexBuffer(self):
        self.CompactTextureList = [0] * self.textureNumber
        for i in range(0, len(self.SortedTextureList)):
            index = self.SortedTextureList[i]
            self.CompactTextureList[index] += 1

    def sortVertices(self):
        self.SortedIndicesList = self.IndicesList.copy()
        self.SortedTextureList = self.TextureList.copy()
        self.sortIndexBuffer()
        self.compactSortedIndexBuffer()

    def CreateCuboid(self, lx, ly, lz, dcx, dcy, dcz, cx, cy, cz, color, texture):
        lx = lx / 2
        ly = ly / 2
        lz = lz / 2
        a = [dcx - lx, dcy + ly, dcz - lz]
        b = [dcx + lx, dcy + ly, dcz - lz]
        c = [dcx + lx, dcy - ly, dcz - lz]
        d = [dcx - lx, dcy - ly, dcz - lz]
        e = [dcx - lx, dcy + ly, dcz + lz]
        f = [dcx + lx, dcy + ly, dcz + lz]
        g = [dcx + lx, dcy - ly, dcz + lz]
        h = [dcx - lx, dcy - ly, dcz + lz]
        self.CreateRectangle(a, b, c, d, cx, cy, cz, color[0], texture[0])
        self.CreateRectangle(e, f, b, a, cx, cy, cz, color[1], texture[1])
        self.CreateRectangle(h, g, f, e, cx, cy, cz, color[2], texture[2])
        self.CreateRectangle(d, c, g, h, cx, cy, cz, color[3], texture[3])
        self.CreateRectangle(b, f, g, c, cx, cy, cz, color[4], texture[4])
        self.CreateRectangle(e, a, d, h, cx, cy, cz, color[5], texture[5])

    def CreateRectangle(self, a, b, c, d, cx, cy, cz, color, texture):
        offset = int(len(self.VerticesList) / self.vertexSize)
        Tex0 = [0, 0, 0]
        Tex1 = [0, 1, 0]
        Tex2 = [1, 1, 0]
        Tex3 = [1, 0, 0]
        positions = numpy.array(
            [a[0], a[1], a[2], Tex0[0], Tex0[1], Tex0[2], cx, cy, cz, 0, 0, 1, color[0], color[1], color[2],
             b[0], b[1], b[2], Tex1[0], Tex1[1], Tex1[2], cx, cy, cz, 0, 0, 1, color[0], color[1], color[2],
             c[0], c[1], c[2], Tex2[0], Tex2[1], Tex2[2], cx, cy, cz, 0, 0, 1, color[0], color[1], color[2],
             d[0], d[1], d[2], Tex3[0], Tex3[1], Tex3[2], cx, cy, cz, 0, 0, 1, color[0], color[1], color[2]],
            dtype='float32')
        faceindices = numpy.array([], dtype='int32')
        i = 0 + offset
        faceindices = numpy.append(faceindices, [i, i + 1, i + 2, i + 2, i + 3, i])
        self.TextureList.append(texture)
        self.TextureList.append(texture)
        self.VerticesList = numpy.append(self.VerticesList, positions)
        self.IndicesList = numpy.append(self.IndicesList, faceindices)

        self.VerticesList = self.VerticesList.astype('float32')
        self.IndicesList = self.IndicesList.astype('int32')

    def CreateCylinder(self, r, h, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture):
        self.CreateCircle(r, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture)
        self.CreateCircle(r, accuracy, dcx, dcy + h, dcz, cx, cy, cz, color, texture)
        self.CreateCylinderEdge(r, h, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture)

    def CreateCircle(self, r, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture):
        if accuracy < 12:
            accuracy = 12
        accuracy = int(accuracy / 4) * 4

        offset = int(len(self.VerticesList) / self.vertexSize)
        indexOffset = len(self.IndicesList)
        angle = (2 * math.pi) / accuracy

        positions = numpy.array(([dcx, dcy, dcz, 0.5, 0.5, 0, cx, cy, cz, 0, 0, 1, color[0], color[1], color[2]]),
                                dtype='float32')
        for i in range(1, accuracy + 1):
            x = (r * math.cos(angle * i)) + dcx
            y = dcy
            z = (r * math.sin(angle * i)) + dcz
            tx = (0.5 * math.cos(angle * i)) + 0.5
            ty = (0.5 * math.sin(angle * i)) + 0.5
            tz = 0
            positions = numpy.append(positions,
                                     [x, y, z, tx, ty, tz, cx, cy, cz, 0, 0, 1, color[0], color[1], color[2]])

        faceindices = numpy.array([], dtype='int32')

        offsetEnd = int(len(positions) / self.vertexSize) - 1

        for i in range(2 + offset, accuracy + 1 + offset):
            faceindices = numpy.append(faceindices, [0 + offset, i - 1, i])
        faceindices = numpy.append(faceindices, [0 + offset, accuracy + offset, 1 + offset])

        indexOffsetEnd = indexOffset + (len(faceindices) - 3)

        textureOffset = len(self.TextureList)

        for i in range(0, accuracy):
            self.TextureList.append(texture)

        textureOffsetEnd = len(self.TextureList) - 1

        self.VerticesList = numpy.append(self.VerticesList, positions)
        self.IndicesList = numpy.append(self.IndicesList, faceindices)

        self.VerticesList = self.VerticesList.astype('float32')
        self.IndicesList = self.IndicesList.astype('int32')

        return [offset, offsetEnd, indexOffset, indexOffsetEnd, textureOffset, textureOffsetEnd]

    def CreateCylinderEdge(self, r, h, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture):
        offset = int(len(self.VerticesList) / self.vertexSize)
        if accuracy < 12:
            accuracy = 12
        accuracy = int(accuracy / 4) * 4
        ratio = 1 / accuracy
        angle = (2 * math.pi) / accuracy

        positions = numpy.array([], dtype='float32')

        for a in range(1, accuracy):
            pointOne = [(r * math.cos(angle * a)) + dcx, dcy + h, (r * math.sin(angle * a)) + dcz]
            pointTwo = [(r * math.cos(angle * a)) + dcx, dcy, (r * math.sin(angle * a)) + dcz]
            pointThree = [(r * math.cos(angle * (a + 1))) + dcx, dcy + h, (r * math.sin(angle * (a + 1))) + dcz]
            pointFour = [(r * math.cos(angle * (a + 1))) + dcx, dcy, (r * math.sin(angle * (a + 1))) + dcz]

            i = [pointTwo[0] - pointOne[0], pointTwo[1] - pointOne[1], pointTwo[2] - pointOne[2]]
            j = [pointThree[0] - pointOne[0], pointThree[1] - pointOne[1], pointThree[2] - pointOne[2]]
            cross = [(i[1] * j[2]) - (i[2] * j[1]), (i[0] * j[2]) - (i[2] * j[0]), (i[0] * j[1]) - (i[1] * j[0])]
            size = (cross[0] * cross[0] + cross[1] * cross[1] + cross[2] * cross[2])
            size = math.sqrt(size)
            cross = [cross[0] / size, cross[1] / size, cross[2] / size]

            tx = 1 - (ratio * a)
            ty = 1
            tz = 0
            positions = numpy.append(positions,
                                     [pointOne[0], pointOne[1], pointOne[2], tx, ty, tz, cx, cy, cz, cross[0], cross[1],
                                      cross[2], color[0], color[1], color[2]])
            ty = 0
            positions = numpy.append(positions,
                                     [pointTwo[0], pointTwo[1], pointTwo[2], tx, ty, tz, cx, cy, cz, cross[0], cross[1],
                                      cross[2], color[0], color[1], color[2]])
            tx = 1 - (ratio * (a - 1))
            ty = 1
            positions = numpy.append(positions,
                                     [pointThree[0], pointThree[1], pointThree[2], tx, ty, tz, cx, cy, cz, cross[0],
                                      cross[1], cross[2], color[0], color[1], color[2]])
            ty = 0
            positions = numpy.append(positions,
                                     [pointFour[0], pointFour[1], pointFour[2], tx, ty, tz, cx, cy, cz, cross[0],
                                      cross[1], cross[2], color[0], color[1], color[2]])

        finalPosition = 4 * accuracy - 5

        faceindices = numpy.array([], dtype='int32')

        for i in range(offset, (finalPosition - 2) + offset):
            faceindices = numpy.append(faceindices, [i, i + 1, i + 2, i + 2, i + 3, i + 1])
        faceindices = numpy.append(faceindices, [finalPosition - 1 + offset, finalPosition + offset,
                                                 offset, offset,
                                                 1 + offset, finalPosition + offset])

        for i in range(0, 2 * (finalPosition - 1)):
            self.TextureList.append(texture)

        self.VerticesList = numpy.append(self.VerticesList, positions)
        self.IndicesList = numpy.append(self.IndicesList, faceindices)

        self.VerticesList = self.VerticesList.astype('float32')
        self.IndicesList = self.IndicesList.astype('int32')

    def CreateCounterHolder(self, r, h, accuracy, l, bltc, trtc, dcx, dcy, dcz, cx, cy, cz, color, texture):
        self.CreateCylinderHole(r, accuracy, l, bltc, trtc, dcx, dcy, dcz, cx, cy, cz, color, texture)
        self.CreateCylinderEdge(r, h, accuracy, dcx, dcy, dcz, cx, cy, cz, color, texture)
        self.CreateCylinderHole(r, accuracy, l, bltc, trtc, dcx, dcy + h, dcz, cx, cy, cz, color, texture)

    def CreateCylinderHole(self, r, accuracy, l, bltc, trtc, dcx, dcy, dcz, cx, cy, cz, color, texture):
        offset = int(len(self.VerticesList) / self.vertexSize)
        blc = [dcx - l / 2, dcz - l / 2]
        trc = [dcx + l / 2, dcz + l / 2]
        if accuracy < 12:
            accuracy = 12
        accuracy = int(accuracy / 4) * 4
        angle = (2 * math.pi) / accuracy
        dcx = (blc[0] + trc[0]) / 2
        dcz = (blc[1] + trc[1]) / 2
        height = abs(trc[1] - blc[1])
        width = abs(trc[0] - blc[0])

        if r > height / 2:
            r = height / 2
        if r > width / 2:
            r = width / 2

        numberOfSpokes = int(accuracy / 4) + 1
        currentSpoke = int(numberOfSpokes / 2) + 1
        method = 0

        positions = numpy.array(([dcx, dcy, dcz, 0.5, 0.5, 0, cx, cy, cz, 0, 1, 0, color[0], color[1], color[2]]),
                                dtype='float32')
        for i in range(1, accuracy + 1):
            x = (r * math.cos(angle * i)) + dcx
            y = dcy
            z = (r * math.sin(angle * i)) + dcz
            largeVector = [trtc[0] - bltc[0], trtc[1] - bltc[1]]

            smallVector = [x - bltc[0], z - bltc[1]]
            textureVector = [smallVector[0] / largeVector[0], smallVector[1] / largeVector[1]]
            tx = textureVector[0]
            ty = textureVector[1]
            tz = 0
            positions = numpy.append(positions,
                                     [x, y, z, tx, ty, tz, cx, cy, cz, 0, 1, 0, color[0], color[1], color[2]])

            newPositions = self.increaseMethod(method, x, y, z, cx, cy, cz, tx, ty, tz, smallVector, largeVector,
                                               textureVector, blc, trc, bltc, color)
            positions = numpy.append(positions, newPositions)

            currentSpoke += 1
            if currentSpoke == numberOfSpokes + 1:
                currentSpoke = 2
                method += 1
                newPositions = self.increaseMethod(method, x, y, z, cx, cy, cz, tx, ty, tz, smallVector, largeVector,
                                                   textureVector, blc, trc, bltc, color)
                positions = numpy.append(positions, newPositions)
                if method == 1:
                    x = trc[0]
                    z = trc[1]
                elif method == 2:
                    x = blc[0]
                    z = trc[1]
                elif method == 3:
                    x = blc[0]
                    z = blc[1]
                else:
                    x = trc[0]
                    z = blc[1]
                smallVector = [x - bltc[0], z - bltc[1]]
                textureVector = [smallVector[0] / largeVector[0], smallVector[1] / largeVector[1]]
                tx = textureVector[0]
                ty = textureVector[1]
                positions = numpy.append(positions,
                                         [x, y, z, tx, ty, tz, cx, cy, cz, 0, 1, 0, color[0], color[1], color[2]])

        currentSpoke = int(numberOfSpokes / 2) + 1
        i = 1 + offset
        faceindices = numpy.array([], dtype='int32')
        while i < (2 * accuracy + 6 + offset):
            faceindices = numpy.append(faceindices, [i, i + 1, i + 2, i + 2, i + 3, i + 1])
            self.TextureList.append(texture)
            self.TextureList.append(texture)
            currentSpoke += 1
            if currentSpoke == numberOfSpokes + 1:
                currentSpoke = 2
                faceindices = numpy.append(faceindices, [i, i + 2, i + 4, i + 4, i + 5, i + 2])
                self.TextureList.append(texture)
                self.TextureList.append(texture)
                i += 2
            i += 2
        faceindices = numpy.append(faceindices, [i, i + 1, 1 + offset, 1 + offset, 2 + offset, i + 1])
        self.TextureList.append(texture)
        self.TextureList.append(texture)

        self.VerticesList = numpy.append(self.VerticesList, positions)
        self.IndicesList = numpy.append(self.IndicesList, faceindices)

        self.VerticesList = self.VerticesList.astype('float32')
        self.IndicesList = self.IndicesList.astype('int32')

    @staticmethod
    def increaseMethod(method, x, y, z, cx, cy, cz, tx, ty, tz, smallVector, largeVector, textureVector, blc, trc, bltc,
                       color):
        if method == 0:
            x = trc[0]
            smallVector[0] = x - bltc[0]
            textureVector[0] = smallVector[0] / largeVector[0]
            tx = textureVector[0]
        elif method == 1:
            z = trc[1]
            smallVector[1] = z - bltc[1]
            textureVector[1] = smallVector[1] / largeVector[1]
            ty = textureVector[1]
        elif method == 2:
            x = blc[0]
            smallVector[0] = x - bltc[0]
            textureVector[0] = smallVector[0] / largeVector[0]
            tx = textureVector[0]
        elif method == 3:
            z = blc[1]
            smallVector[1] = z - bltc[1]
            textureVector[1] = smallVector[1] / largeVector[1]
            ty = textureVector[1]
        else:
            x = trc[0]
            smallVector[0] = x - bltc[0]
            textureVector[0] = smallVector[0] / largeVector[0]
            tx = textureVector[0]
        Result = [x, y, z, tx, ty, tz, cx, cy, cz, 0, 1, 0, color[0], color[1], color[2]]
        return Result
