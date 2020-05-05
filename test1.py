import numpy as n
import ast
import Game as G

r = 0
c = 0
while r < 10 or c < 10:
    print("There should be at least 10 rows and columns!")
    r = int(input("Enter the number of rows: "))
    c = int(input("Enter the number of columns: "))
g = G.Game(r, c)

while not g.full():
    g.show_state()
    if g.turn() == 1:
        g.show_state()
        break
    g.player_switch()
g.show_state()