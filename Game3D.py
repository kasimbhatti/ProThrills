import numpy as n
import copy


class Game3D:
    def __init__(self, r, c, h):
        self.board = n.zeros([r, c, h])
        self.rows = r
        self.cols = c
        self.height = h
        self.player = 1
        self.test_mode = False

    def turn(self):
        h = -2
        while h == -2:
            c = int(input("enter the column: ")) - 1
            while (c < 0) or (c >= self.cols):
                print("Invalid column!")
                c = int(input("enter the column: ")) - 1
            r = int(input("enter the row: ")) - 1
            while (r < 0) or (r >= self.rows):
                print("Invalid row!")
                r = int(input("enter the row: ")) - 1

            h = self.add(r, c, self.player)
        return self.check_score(r, c, h)

    def player_switch(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1
        return None

    def return_player(self):
        return self.player

    def height_full(self, r, c):
        tf = True
        for i in range(self.rows):
            tf = tf and (self.board[r][c][i] != 0)
        return tf

    def add(self, r,  c, player):  # Returns the i coordinate for the column (used as the r_target value for check_score)
        idx = -1               # if the add is valid, else returns -1
        if self.height_full(r, c):
            print("This slot is full!")
            return -2
        for i in range(self.height - 1, -1, -1):
            if self.board[r][c][i] == 0:
                idx = i
                break
        if idx >= 0:
            self.board[r][c][idx] = player
        return idx

    def newTurn(self, r, c, h):
        return self.check_score(r, c, h)

    def check_full_score(self):
        if self.row_score(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.col_score(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.height_score(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score1(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score2(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score3(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score4(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score5(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.diagonal_score6(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.super_diagonal1(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.super_diagonal2(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.super_diagonal3(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        if self.super_diagonal4(self.board, self.rows, self.cols, self.height) == 1:
            return 1
        return 0

    def check_score(self, r_target, c_target, h_target):
        r_dist = self.row_edge_dist(r_target)
        c_dist = self.col_edge_dist(c_target)
        h_dist = self.height_edge_dist(h_target)
        for a in range(min(4, r_dist + 1)):
            for b in range(min(4, c_dist + 1)):
                for c in range(min(4, h_dist + 1)):
                    new_board = self.copy_board(r_target, c_target, h_target, a, b, c, 3, 3, 3)
                    if self.row_score(new_board, 4, 4, 4) == 1:  # If 4 are connected in a row
                        return 1  # Win state
                    if self.col_score(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.height_score(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score1(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score2(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score3(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score3(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score4(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score5(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.diagonal_score6(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.super_diagonal1(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.super_diagonal2(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.super_diagonal3(new_board, 4, 4, 4) == 1:
                        return 1
                    if self.super_diagonal4(new_board, 4, 4, 4) == 1:
                        return 1
        return 0

    def copy_board(self, r_target, c_target, h_target, a, b, c, r_dist, c_dist, h_dist):

        new_board = n.zeros([4, 4, 4])
        for i in range(0, 4):
            for j in range(0, 4):
                for k in range(0, 4):
                    new_board[i][j][k] = copy.deepcopy(self.board[i + r_target + a - r_dist][j + c_target + b - c_dist][k + h_target + c - h_dist])

        return new_board

    def full(self):
        tf = False
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                for k in range(0, self.height):
                    tf = tf or (self.board[i][j][k] == 0)
        return not tf

    def col_score(self, board, row, col, height):
        for h in range(height):
            for i in range(row):
                count = 0
                for j in range(col):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        for r in range(row):
            for h in range(height):
                count = 0
                for j in range(col):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def row_score(self, board, row, col, height):
        for h in range(height):
            for j in range(col):
                count = 0
                for i in range(row):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        for j in range(col):
            for h in range(height):
                count = 0
                for i in range(row):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def height_score(self, board, row, col, height):
        for i in range(row):
            for j in range(col):
                count = 0
                for h in range(height):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        for j in range(col):
            for i in range(row):
                count = 0
                for h in range(height):
                    if board[i][j][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score1(self, board, row, col, height):
        for h in range(height):
            for r in range(row):
                count = 0
                c = 0
                while r <= row - 1 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r += 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
            for c in range(col):
                count = 0
                r = 0
                while r <= row - 1 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r += 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score2(self, board, row, col, height):
        for h in range(height):
            for r in range(row - 1, -1, -1):
                count = 0
                c = 0
                while r >= 0 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r -= 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1

            for c in range(col):
                count = 0
                r = row - 1
                while r >= 0 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r -= 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score3(self, board, row, col, height):
        for r in range(row):
            for h in range(height):
                count = 0
                c = 0
                while h <= height - 1 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h += 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
            for c in range(col):
                count = 0
                h = 0
                while h <= height - 1 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h += 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score4(self, board, row, col, height):
        for r in range(row):
            for h in range(height - 1, -1, -1):
                count = 0
                c = 0
                while h >= 0 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h -= 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1

            for c in range(col):
                count = 0
                h = height - 1
                while h >= 0 and c <= col - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h -= 1
                    c += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score5(self, board, row, col, height):
        for c in range(col):
            for r in range(row):
                count = 0
                h = 0
                while r <= row - 1 and h <= height - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r += 1
                    h += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
            for h in range(height):
                count = 0
                r = 0
                while r <= row - 1 and h <= height - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    r += 1
                    h += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def diagonal_score6(self, board, row, col, height):
        for c in range(col):
            for h in range(height - 1, -1, -1):
                count = 0
                r = 0
                while h >= 0 and r <= row - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h -= 1
                    r += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1

            for r in range(row):
                count = 0
                h = height - 1
                while h >= 0 and r <= row - 1:
                    if board[r][c][h] == self.player:
                        count += 1
                    else:
                        count = 0
                    h -= 1
                    r += 1
                    if count == 4:
                        print("Player %d wins!" % self.player)
                        return 1
        return 0

    def super_diagonal1(self, board, row, col, height):
        for r in range(row):
            count = 0
            c = 0
            h = 0
            while r <= row - 1 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for c in range(col):
            count = 0
            r = 0
            h = 0
            while r <= row - 1 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for h in range(height):
            count = 0
            r = 0
            c = 0
            while r <= row - 1 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def super_diagonal2(self, board, row, col, height):
        for r in range(row - 1, -1, -1):
            count = 0
            c = 0
            h = 0
            while r >= 0 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for c in range(col):
            count = 0
            r = row - 1
            h = 0
            while r >= 0 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for h in range(height):
            count = 0
            r = row - 1
            c = 0
            while r >= 0 and c <= col - 1 and h <= height -1:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def super_diagonal3(self, board, row, col, height):
        for r in range(row):
            count = 0
            c = 0
            h = height - 1
            while r <= row - 1 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for c in range(col):
            count = 0
            r = 0
            h = height - 1
            while r <= row - 1 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for h in range(height - 1, -1, -1):
            count = 0
            r = 0
            c = 0
            while r <= row - 1 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def super_diagonal4(self, board, row, col, height):
        for r in range(row - 1, -1, -1):
            count = 0
            c = 0
            h = height - 1
            while r >= 0 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for c in range(col):
            count = 0
            r = row - 1
            h = height - 1
            while r >= 0 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        for h in range(height - 1, -1, -1):
            count = 0
            r = row - 1
            c = 0
            while r >= 0 and c <= col - 1 and h >= 0:
                if board[r][c][h] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                h -= 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def row_edge_dist(self, r):
        return min(r, self.rows - 1 - r)

    def col_edge_dist(self, co):
        return min(co, self.cols - 1 - co)

    def height_edge_dist(self, height):
        return min(height, self.height - 1 - height)

    def show_state(self):
        print(self.board)
