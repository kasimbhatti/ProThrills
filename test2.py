import numpy as n
import ast
import Game3D as G3

r = 0
c = 0
h = 0
while r < 10 or c < 10 or h < 10:
    print("The board should be at least 10x10x10 !")
    r = int(input("Enter the number of rows: "))
    c = int(input("Enter the number of columns: "))
    h = int(input("Enter the height of the board: "))
g = G3.Game3D(r, c, h)

while not g.full():
    g.show_state()
    if g.turn() == 1:
        g.show_state()
        break
    g.player_switch()
g.show_state()