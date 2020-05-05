import numpy as n
import copy


class Game:
    def __init__(self, r, c):
        self.board = n.zeros([r, c])
        self.rows = r
        self.cols = c
        self.player = 1
        self.test_mode = False

    def test_board(self, t):
        if t == 0:
            self.board = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10)],
                          [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10)],
                          [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10)],
                          [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10)],
                          [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10)],
                          [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10)],
                          [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10)],
                          [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 7), (7, 9), (7, 10)],
                          [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10)],
                          [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10)],
                          [(10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]]
            self.rows = 11
            self.cols = 11
        else:
            self.board = [[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                          [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
                          [2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8],
                          [3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8],
                          [4, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8],
                          [5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8],
                          [6, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8],
                          [7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8],
                          [8, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8]]
            self.rows = 9
            self.cols = 9
        self.player = 1
        self.test_mode = True

    def turn(self):
        r = -2
        while r == -2:
            c = int(input("enter the column: ")) - 1
            while (c < 0) or (c >= self.cols):
                print("Invalid row!")
                c = int(input("enter the column: ")) - 1

            r = self.add(c, self.player)
        return self.check_score(r, c)

    def player_switch(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1
        return None

    def col_full(self, col):
        tf = True
        for i in range(self.rows):
            tf = tf and (self.board[i][col] != 0)
        return tf

    def add(self, c, player):  # Returns the i coordinate for the column (used as the r_target value for check_score)
        idx = -1               # if the add is valid, else returns -1
        if self.col_full(c):
            print("This column is full!")
            return -2
        for i in range(self.rows - 1, -1, -1):
            if self.board[i][c] == 0:
                idx = i
                break
        if idx >= 0:
            self.board[idx][c] = player
        return idx

    def check_full_score(self):
        if self.row_score(self.board, self.rows, self.cols) == 1:
            return 1
        if self.col_score(self.board, self.rows, self.cols) == 1:
            return 1
        if self.diagonal_score1(self.board, self.rows, self.cols) == 1:
            return 1
        if self.diagonal_score2(self.board, self.rows, self.cols) == 1:
            return 1
        return 0

    def check_score(self, r_target, c_target):
        r_dist = self.row_edge_dist(r_target)
        c_dist = self.col_edge_dist(c_target)
        for a in range(min(4, r_dist + 1)):
            for b in range(min(4, c_dist + 1)):
                new_board = self.copy_board(r_target, c_target, a, b, 3, 3)
                #  one = self.row_score(new_board)
                if self.row_score(new_board, 4, 4) == 1:  # If 4 are connected in a row
                    return 1  # Win state
                #  one = self.col_score(new_board)
                if self.col_score(new_board, 4, 4) == 1:
                    return 1
                #  one = self.diagonal_score1(new_board)
                if self.diagonal_score1(new_board, 4, 4) == 1:
                    return 1
                #  one = self.diagonal_score2(new_board)
                if self.diagonal_score2(new_board, 4, 4) == 1:
                    return 1
        return 0

    def copy_board(self, r_target, c_target, a, b, r_dist, c_dist):
        # new_board = [[0, 0, 0, 0],
        #              [0, 0, 0, 0],
        #              [0, 0, 0, 0],
        #              [0, 0, 0, 0]]
        new_board = n.zeros([4, 4])
        for i in range(0, 4):
            for j in range(0, 4):
                new_board[i][j] = copy.deepcopy(self.board[i + r_target + a - r_dist][j + c_target + b - c_dist])
        return new_board

    def full(self):
        tf = False
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                tf = tf or (self.board[i][j] == 0)
        return not tf

    def row_score(self, board, row, col):
        for i in range(row):
            count = 0
            for j in range(col):
                if board[i][j] == self.player:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def col_score(self, board, row, col):
        for j in range(col):
            count = 0
            for i in range(row):
                if board[i][j] == self.player:
                    count += 1
                else:
                    count = 0
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def diagonal_score1(self, board, row, col):
        for r in range(row):
            count = 0
            c = 0
            while r <= row - 1 and c <= col - 1:
                if board[r][c] == self.player:
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
                if board[r][c] == self.player:
                    count += 1
                else:
                    count = 0
                r += 1
                c += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def diagonal_score2(self, board, row, col):
        for r in range(row - 1, -1, -1):
            count = 0
            c = 0
            while r >= 0 and c <= col - 1:
                if board[r][c] == self.player:
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
                if board[r][c] == self.player:
                    count += 1
                else:
                    count = 0
                r -= 1
                c += 1
                if count == 4:
                    print("Player %d wins!" % self.player)
                    return 1
        return 0

    def row_edge_dist(self, r):
        return min(r, self.rows - 1 - r)

    def col_edge_dist(self, co):
        return min(co, self.cols - 1 - co)

    def show_state(self):
        print(self.board)
