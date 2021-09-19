import numpy as np
import math
import requests

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
board = response.json()['board']

player_board = [[0,0,0,0,0,0,0,0,0], 
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

solved_board = [[0,0,0,0,0,0,0,0,0], 
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

def is_valid(row, column, number):
    global solved_board
    for i in range(0, 9):
        if solved_board[row][i] == number:
            return False
    for j in range(0, 9):
        if solved_board[j][column] == number:
            return False
    box_x = math.floor(row/3)  
    box_y = math.floor(column/3)
    for k in range(0, 3):
        for l in range(0, 3):
            if solved_board[box_x*3 + k][box_y*3 + l] == number:
                return False
    return True
        
def solve():
    global solved_board
    for row in range(0,9):
        for column in range(0,9):
            if solved_board[row][column] == 0:
                for num in range(1,10):
                    if is_valid(row, column, num):
                        solved_board[row][column]=num
                        if solve():
                            return True
                    solved_board[row][column] = 0
                return False
    return True       

def create_player_board():
    for i in range(0,9):
        for j in range(0,9):
            player_board[i][j] = board[i][j]
            solved_board[i][j] = board[i][j]
  
#create_player_board()
#solve()
#print(np.matrix(solved_board))
#print(np.matrix(player_board))

