import glfw
from Renderer import Renderer
import math as m
from ObjectLibrary import ObjectLibrary
from Game3D import Game3D


def multiplyQuaternions(QuatL, QuatR):
    Result = [QuatL[3] * QuatR[0] + QuatL[0] * QuatR[3] + QuatL[2] * QuatR[1] - QuatL[1] * QuatR[2],
              QuatL[3] * QuatR[1] + QuatL[1] * QuatR[3] + QuatL[0] * QuatR[2] - QuatL[2] * QuatR[0],
              QuatL[3] * QuatR[2] + QuatL[2] * QuatR[3] + QuatL[1] * QuatR[0] - QuatL[0] * QuatR[1],
              QuatL[3] * QuatR[3] - QuatL[0] * QuatR[0] - QuatL[1] * QuatR[1] - QuatL[2] * QuatR[2]]
    return Result


def normalizeQuaternion(Quat):
    Size = Quat[0] * Quat[0] + Quat[1] * Quat[1] + Quat[2] * Quat[2] + Quat[3] * Quat[3]
    Size = m.sqrt(Size)
    NewQuat = [Quat[0] / Size, Quat[1] / Size, Quat[2] / Size, Quat[3] / Size]
    return NewQuat


def clicked(window, KEY, last, override):
    if override:
        entered = False
    else:
        entered = False
        if glfw.get_key(window, KEY) == glfw.PRESS:
            if not last:
                entered = True
            last = True
        else:
            last = False
    return [entered, last]


def receiveInputCounter(window, number, KEY, last, currentNumber, override):
    enterList = clicked(window, KEY, last, override)
    last = enterList[1]
    entered = enterList[0]
    if entered:
        if currentNumber != -1:
            currentNumber *= 10
            currentNumber += number
        else:
            currentNumber = number
    return [entered, last, currentNumber]


def main():
    rows = 0
    columns = 0
    height = 0
    while rows < 5 or columns < 5 or height < 5:
        print("The board should be at least 5 x 5 x 5 !  Make sure your inputs are numeric")
        try:
            rows = int(input("Enter an odd number of rows: "))
            columns = int(input("Enter an odd number of columns: "))
            height = int(input("Enter an odd number of layers: "))
        except ValueError:
            rows = 0
            columns = 0
            height = 0
    if rows % 2 == 0:
        rows += 1
    if columns % 2 == 0:
        columns += 1
    if height % 2 == 0:
        height += 1
    print("Game initiated with size " + str(rows) + " x " + str(columns) + " x " + str(height))
    print("")
    print("Use the mouse whilst holding the left click button to rotate the arena")
    print("Use the WASD keys to control movement of the arena")
    print("When selecting a place for your counter, type the row number first, and click enter, then type the column number next, and click enter. If the rows and"
          " columns chosen are valid, then the counter will be placed in the bottom layer")
    print("If a counter is already placed in that position in the layer, then the counter will be placed one layer higher than it")
    print("Connect 4's can be found in all 3 dimensions, so watch out for diagonal connects between layers!")
    print("Once a connect has been made, the game will end and a white line will display the positions of the connected counters on the screen")
    print("Good luck and remember to have fun!")

    print("Graphics by Kasim Rehman Bhatti, game mechanics by Atharva Vadeyar, server hosting by Tillega Narayanan")
    print("This game was created using Python for both the machnics and graphics of the game. The graphics work by using Modern OpenGL")
    NewGame = Game3D(rows, columns, height)

    WindowName = "OpenGL Testing"
    if not glfw.init():
        return
    ScreenWidth = 1920
    ScreenHeight = 1080
    window = glfw.create_window(ScreenWidth, ScreenHeight, WindowName, None, None)
    Scale = 0.5
    Ratio = ScreenWidth / ScreenHeight
    ScaledRatio = Scale * Ratio
    if not window:
        glfw.terminate()
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    NewRender = Renderer()

    NewRender.AddShader("Shaders\Complete Shader")
    textureNumber = NewRender.attachTextures("Textures")
    vertexSize = NewRender.returnVertexSize()
    NewObjectLibrary = ObjectLibrary(textureNumber, vertexSize)

    oxpos = 0
    oypos = 0

    Change = 0.05
    ChangeTX = 0.00
    ChangeTY = 0.00
    ChangeTZ = 0.00

    CurrentQuaternion = [0, 0, 0, 1]
    First = True

    multiplier = (rows * columns) / 40
    if (rows * columns) < 40:
        multiplier = 1

    radius = 0.27
    depth = 0.05
    accuracy = 60
    length = 0.7
    objectCentre = [0, 0, -4]
    rotationCentre = [0, 0, -4]
    texture = 2
    color = [0, 0, 0.4]
    counterTexture = 3
    counterColor1 = [0.7, 0, 0]
    counterColor2 = [0.7, 0.7, 0]

    bltc = [objectCentre[0] + (- (rows / 2)) * length, objectCentre[2] + (- (columns / 2)) * length]
    trtc = [objectCentre[0] + (rows / 2) * length, objectCentre[2] + (columns / 2) * length]
    for k in range(0, int(height)):
        for j in range(-int(rows / 2), int(rows / 2) + 1):
            for i in range(-int(columns / 2), int(columns / 2) + 1):
                NewObjectLibrary.CreateCounterHolder(radius, depth, accuracy, length, bltc, trtc,
                                                     objectCentre[0] + j * length, objectCentre[1] + (k * multiplier),
                                                     objectCentre[2] + i * length, rotationCentre[0],
                                                     rotationCentre[1], rotationCentre[2], color, texture)
                a = [objectCentre[0] - ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] - ((columns * length) / 2)]
                b = [objectCentre[0] + ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] - ((columns * length) / 2)]
                c = [objectCentre[0] + ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] - ((columns * length) / 2)]
                d = [objectCentre[0] - ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] - ((columns * length) / 2)]
                NewObjectLibrary.CreateRectangle(a, b, c, d, objectCentre[0], objectCentre[1], objectCentre[2], color,
                                                 texture)
                a = [objectCentre[0] - ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] + ((columns * length) / 2)]
                b = [objectCentre[0] + ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] + ((columns * length) / 2)]
                c = [objectCentre[0] + ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] + ((columns * length) / 2)]
                d = [objectCentre[0] - ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] + ((columns * length) / 2)]
                NewObjectLibrary.CreateRectangle(a, b, c, d, objectCentre[0], objectCentre[1], objectCentre[2], color,
                                                 texture)
                a = [objectCentre[0] + ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] + ((columns * length) / 2)]
                b = [objectCentre[0] + ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] - ((columns * length) / 2)]
                c = [objectCentre[0] + ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] - ((columns * length) / 2)]
                d = [objectCentre[0] + ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] + ((columns * length) / 2)]
                NewObjectLibrary.CreateRectangle(a, b, c, d, objectCentre[0], objectCentre[1], objectCentre[2], color,
                                                 texture)
                a = [objectCentre[0] - ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] + ((columns * length) / 2)]
                b = [objectCentre[0] - ((rows * length) / 2), objectCentre[1] + (k * multiplier) + depth,
                     objectCentre[2] - ((columns * length) / 2)]
                c = [objectCentre[0] - ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] - ((columns * length) / 2)]
                d = [objectCentre[0] - ((rows * length) / 2), (k * multiplier),
                     objectCentre[2] + ((columns * length) / 2)]
                NewObjectLibrary.CreateRectangle(a, b, c, d, objectCentre[0], objectCentre[1], objectCentre[2], color,
                                                 texture)

    color = [[0, 0, 0.4], [0, 0, 0.4], [0, 0, 0.4], [0, 0, 0.4], [0, 0, 0.4], [0, 0, 0.4]]
    texture = [2, 2, 2, 2, 2, 2]
    NewObjectLibrary.CreateCuboid(rows * length + 2, depth, columns * length, objectCentre[0], objectCentre[1] - 1,
                                  objectCentre[2], rotationCentre[0], rotationCentre[1], rotationCentre[2], color,
                                  texture)
    NewObjectLibrary.CreateCuboid(0.1, 2 * depth, columns * length, objectCentre[0] - ((rows * length) / 2),
                                  objectCentre[1] - 1 + depth,
                                  objectCentre[2], rotationCentre[0], rotationCentre[1], rotationCentre[2], color,
                                  texture)
    NewObjectLibrary.CreateCuboid(0.1, 2 * depth, columns * length, objectCentre[0] + ((rows * length) / 2),
                                  objectCentre[1] - 1 + depth,
                                  objectCentre[2], rotationCentre[0], rotationCentre[1], rotationCentre[2], color,
                                  texture)

    for i in range(-int(columns / 2), int(columns / 2) + 1):
        NewObjectLibrary.CreateCylinder(radius, depth, accuracy,
                                        objectCentre[0] - ((rows * length) / 2) - 0.5, objectCentre[1] - 1 + depth,
                                        objectCentre[2] + i * length, rotationCentre[0],
                                        rotationCentre[1], rotationCentre[2], counterColor1, counterTexture)

    for i in range(-int(columns / 2), int(columns / 2) + 1):
        NewObjectLibrary.CreateCylinder(radius, depth, accuracy,
                                        objectCentre[0] + ((rows * length) / 2) + 0.5, objectCentre[1] - 1 + depth,
                                        objectCentre[2] + i * length, rotationCentre[0],
                                        rotationCentre[1], rotationCentre[2], counterColor2, counterTexture)

    NewObjectLibrary.sortVertices()

    FOVradians = 1
    Near = 3
    Far = -1

    Done = False

    currentNumber = -1
    currentNumberBuffer = [-1, -1]

    lastBackspace = False
    lastEnter = False
    currentIndex = 0
    last = [False, False, False, False, False, False, False, False, False, False]
    lastclicked = False

    connectFound = False
    startBuffer = [-1, -1, -1]
    endBuffer = [-1, -1, -1]

    NewGame.show_state()

    override = False

    while not glfw.window_should_close(window) and not Done:
        NewRender.ProjectAndStretch(FOVradians, Near, Far, Scale, ScaledRatio)

        if glfw.get_key(window, glfw.KEY_Q) == glfw.PRESS:
            Done = True
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            ChangeTX += Change
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            ChangeTY += Change
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            ChangeTX -= Change
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            ChangeTY -= Change
        if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
            ChangeTZ -= Change
        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            ChangeTZ += Change

        enterList = clicked(window, glfw.KEY_ENTER, lastEnter, override)
        lastEnter = enterList[1]
        enter = enterList[0]

        enterList = clicked(window, glfw.KEY_BACKSPACE, lastBackspace, override)
        lastBackspace = enterList[1]
        backspace = enterList[0]
        if backspace:
            if currentNumber == 0:
                currentNumber = -1
            elif currentNumber != -1:
                currentNumber /= 10
                currentNumber = int(currentNumber)

        for i in range(0, 10):
            enterList = receiveInputCounter(window, 0 + i, glfw.KEY_0 + i, last[i], currentNumber, override)
            currentNumber = enterList[2]
            last[i] = enterList[1]

        if enter:
            if currentNumber != -1:
                currentNumberBuffer[currentIndex] = currentNumber
                currentIndex += 1
                currentNumber = -1

        if currentIndex == 2:
            currentIndex = 0

        if currentNumberBuffer[0] != -1 and currentNumberBuffer[1] != -1 and not connectFound:
            EnteredRow = False
            EnteredColumn = False
            if currentNumberBuffer[0] > rows - 1:
                print("invalid row")
            else:
                EnteredRow = True
            if currentNumberBuffer[1] > columns - 1:
                print("invalid column")
            else:
                EnteredColumn = True

            initialPlayer = NewGame.return_player()
            if EnteredRow and EnteredColumn:
                added = NewGame.add(currentNumberBuffer[0], currentNumberBuffer[1], initialPlayer)
                newHeight = height - (added + 1)

                (turn, arrays) = NewGame.newTurn(currentNumberBuffer[0], currentNumberBuffer[1], newHeight)
                if turn == 1:
                    connectFound = True
                    startBuffer = arrays[0]
                    startBuffer[2] = -(startBuffer[2] + 1)
                    endBuffer = arrays[1]
                    endBuffer[2] = -(endBuffer[2] + 1)
                    print(startBuffer)
                    print(endBuffer)

                if added != -1 and added != -2:
                    if initialPlayer == 1:
                        counterColor = counterColor1
                    else:
                        counterColor = counterColor2

                    NewObjectLibrary.CreateCylinder(radius, depth, accuracy,
                                                    objectCentre[0] + (
                                                            (currentNumberBuffer[0] - int(rows / 2)) * length),
                                                    objectCentre[1] + (newHeight * multiplier),
                                                    objectCentre[2] + (
                                                            (currentNumberBuffer[1] - int(columns / 2)) * length),
                                                    rotationCentre[0],
                                                    rotationCentre[1], rotationCentre[2], counterColor, counterTexture)
                    NewObjectLibrary.sortVertices()

                    NewGame.player_switch()

                    print("")
                    print("New state")
                    NewGame.show_state()

                    currentNumber = -1
                    currentNumberBuffer = [-1, -1]

                else:
                    currentNumberBuffer = [-1, -1]
            else:
                currentNumber = -1
                currentNumberBuffer = [-1, -1]

        if connectFound:
            if startBuffer[0] != -1 and startBuffer[1] != -1 and startBuffer[2] != -1:
                if startBuffer[0] > rows - 1:
                    startBuffer[0] = rows - 1
                if startBuffer[1] > columns - 1:
                    startBuffer[1] = columns - 1
                if startBuffer[2] > height - 1:
                    startBuffer[2] = height - 1

                if endBuffer[0] != -1 and endBuffer[1] != -1 and endBuffer[2] != -1:
                    if endBuffer[0] > rows - 1:
                        endBuffer[0] = rows - 1
                    if endBuffer[1] > columns - 1:
                        endBuffer[1] = columns - 1
                    if endBuffer[2] > height - 1:
                        endBuffer[2] = height - 1

                a = [objectCentre[0] + ((startBuffer[0] - int(rows / 2)) * length),
                     objectCentre[1] + (startBuffer[2] * multiplier) + 0.2,
                     objectCentre[2] + ((startBuffer[1] - int(columns / 2)) * length + 0.05)]
                b = [objectCentre[0] + ((startBuffer[0] - int(rows / 2)) * length),
                     objectCentre[1] + (startBuffer[2] * multiplier) + 0.2,
                     objectCentre[2] + ((startBuffer[1] - int(columns / 2)) * length - 0.05)]
                d = [objectCentre[0] + ((endBuffer[0] - int(rows / 2)) * length),
                     objectCentre[1] + (endBuffer[2] * multiplier) + 0.2,
                     objectCentre[2] + ((endBuffer[1] - int(columns / 2)) * length + 0.05)]
                c = [objectCentre[0] + ((endBuffer[0] - int(rows / 2)) * length),
                     objectCentre[1] + (endBuffer[2] * multiplier) + 0.2,
                     objectCentre[2] + ((endBuffer[1] - int(columns / 2)) * length - 0.05)]
                NewObjectLibrary.CreateRectangle(a, b, c, d, objectCentre[0], objectCentre[1], objectCentre[2],
                                                 [1, 1, 1],
                                                 counterTexture)

                NewObjectLibrary.sortVertices()
                connectFound = False

        xypos = glfw.get_cursor_pos(window)
        xpos = xypos[0]
        ypos = xypos[1]
        click = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)

        if click == glfw.PRESS:
            clickbool = True
        else:
            clickbool = False

        if clickbool and lastclicked:
            Deltay = xpos - oxpos
            Deltax = ypos - oypos

            AngleX = 0.00
            AngleY = 0.00

            if Deltay < 0:
                AngleY = Change * 120 * (-Deltay / ScreenHeight)
            elif Deltay > 0:
                AngleY = Change * 120 * (-Deltay / ScreenHeight)
            if Deltax < 0:
                AngleX = Change * 240 * (-Deltax / ScreenWidth)
            elif Deltax > 0:
                AngleX = Change * 240 * (-Deltax / ScreenWidth)

            Quat = [m.sin(AngleX / 2) * m.cos(AngleY / 2),
                    m.sin(AngleY / 2) * m.cos(AngleX / 2),
                    m.sin(AngleX / 2) * m.sin(AngleY / 2),
                    m.cos(AngleX / 2) * m.cos(AngleY / 2)]

            if First:
                CurrentQuaternion = Quat
                CurrentQuaternion = normalizeQuaternion(CurrentQuaternion)
                First = False
            else:
                CurrentQuaternion = multiplyQuaternions(Quat, CurrentQuaternion)
                CurrentQuaternion = normalizeQuaternion(CurrentQuaternion)

        NewRender.RotateQuaternion(CurrentQuaternion)
        NewRender.Translate(ChangeTX, ChangeTY, ChangeTZ)
        NewRender.Lighting(0, 2, 2)
        NewRender.Draw3D(NewObjectLibrary.returnVertices())

        oxpos = xpos
        oypos = ypos
        lastclicked = clickbool

        glfw.swap_buffers(window)
        glfw.poll_events()
    glfw.terminate()


if __name__ == '__main__':
    main()
