import SudokuSolver
import pygame
import sys
import requests

WIDTH = 550
HEIGHT = 650
SMALL_BOX_WIDTH = 50
BLACK = (0,0,0)
WHITE = (255, 255, 255)
TAN = (227, 214, 150)
CORRECT_GREEN = (155, 245, 66)
INCORRECT_RED = (245, 75, 66)
BUTTON_COLOUR = (235, 226, 183)
BUTTON_OUTLINE = (207, 193, 128)
PLAYER_COLOUR = (92, 83, 40)
ASCII_ADJUSTMENT = 48
X_BUFFER = 15

pygame.init()
pygame.display.set_caption("Play Sudoku!")
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
MYFONT = pygame.font.SysFont('Century Gothic', 35)
BUTTON_FONT = pygame.font.SysFont('Century Gothic', 16)
WINNER_FONT = pygame.font.SysFont('Century Gothic', 20)

WIN.fill(TAN)
pygame.display.update()


def draw_board():
    for i in range(0,10):
        if(i%3 == 0):
            pygame.draw.line(WIN, BLACK, (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(WIN, BLACK, (50, 50 + 50*i), (500, 50 + 50*i), 4)
    
        pygame.draw.line(WIN, BLACK, (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(WIN, BLACK, (50, 50 + 50*i), (500, 50 + 50*i), 2)

    clear_text = MYFONT.render("Clear", True, BLACK)
    check_text = MYFONT.render("Check", True, BLACK)
    solve_text = MYFONT.render("Solve", True, BLACK)
    intro_text = MYFONT.render("Sudoku!", True, BLACK)
    next_text = BUTTON_FONT.render("New Board", True, BLACK)
    WIN.blit(intro_text, (210, 10))
    pygame.draw.rect(WIN, BUTTON_OUTLINE, (400, 5, 100, 35))
    pygame.draw.rect(WIN, BUTTON_OUTLINE, (25, 525, 155, 55))
    pygame.draw.rect(WIN, BUTTON_OUTLINE, (200, 525, 155, 55))
    pygame.draw.rect(WIN, BUTTON_OUTLINE, (375, 525, 155, 55))
    pygame.draw.rect(WIN, BUTTON_COLOUR, (400, 5, 95, 30))
    pygame.draw.rect(WIN, BUTTON_COLOUR, (25, 525, 150, 50))
    pygame.draw.rect(WIN, BUTTON_COLOUR, (200, 525, 150, 50))
    pygame.draw.rect(WIN, BUTTON_COLOUR, (375, 525, 150, 50))
    WIN.blit(check_text, (40, 525))
    WIN.blit(solve_text, (225, 525))
    WIN.blit(clear_text, (400, 525))
    WIN.blit(next_text, (405, 10))
    pygame.display.update()


def draw_base_numbers():
    for i in range(0,9):
        for j in range(0,9):
            if(0 < SudokuSolver.player_board[i][j] < 10):
                pygame.draw.rect(WIN, TAN, ((j+1)*50, (i+1)*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
                value = MYFONT.render(str(SudokuSolver.player_board[i][j]), True, BLACK)
                WIN.blit(value, ((j+1)*50 + X_BUFFER, (i+1)*50))


def insert_number(position):
    i, j = position[1], position[0]

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if(SudokuSolver.board[i-1][j-1] != 0):
                    return
            
                elif(event.key == pygame.K_BACKSPACE):
                    SudokuSolver.player_board[i-1][j-1] = 0
                    pygame.draw.rect(WIN, TAN, (position[0]*50, position[1]*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
                    pygame.display.update()
                
                elif(0 < event.key - ASCII_ADJUSTMENT < 10):
                    SudokuSolver.player_board[i-1][j-1] = event.key - ASCII_ADJUSTMENT
                    pygame.draw.rect(WIN, TAN, (position[0]*50, position[1]*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
                    number = MYFONT.render(str(event.key - ASCII_ADJUSTMENT), True, PLAYER_COLOUR)
                    WIN.blit(number, (position[0]*50 + X_BUFFER, position[1]*50))
                    pygame.display.update()

                # elif(event.key == pygame.K_COMMA):
                #     pygame.draw.rect(WIN, TAN, (0, 600, 550, 50))
                #     clear()

                # elif(event.key == pygame.K_PERIOD):
                #     check()
                return


def current_box(position):
    if SudokuSolver.board[(position[1]-1)][(position[0]-1)] != 0:
        return "invalid_spot"
    pygame.draw.rect(WIN, PLAYER_COLOUR, (position[0]*50, position[1]*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
    pygame.draw.rect(WIN, TAN, (position[0]*50 + 5, position[1]*50 + 5, SMALL_BOX_WIDTH - 10, SMALL_BOX_WIDTH -10))
    pygame.display.update()

def clear():
    for i in range(0,9):
        for j in range(0,9):
            if SudokuSolver.board[i][j] == 0:
                SudokuSolver.player_board[i][j] = 0
                pygame.draw.rect(WIN, TAN, ((j+1)*50, (i+1)*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
    draw_base_numbers()

def solve():
    #SudokuSolver.solve()
    for i in range(0,9):
        for j in range(0,9):
            pygame.draw.rect(WIN, TAN, ((j+1)*50, (i+1)*50, SMALL_BOX_WIDTH, SMALL_BOX_WIDTH))
            value = MYFONT.render(str(SudokuSolver.solved_board[i][j]), True, BLACK)
            WIN.blit(value, ((j+1)*50 + X_BUFFER, (i+1)*50))

def check():
    mistakes = 0
    for i in range(0,9):
        for j in range(0,9):
            if SudokuSolver.player_board[i][j] == SudokuSolver.solved_board[i][j]:
                pygame.draw.rect(WIN, CORRECT_GREEN, ((j+1)*50, (i+1)*50, SMALL_BOX_WIDTH , SMALL_BOX_WIDTH ))
                number = MYFONT.render(str(SudokuSolver.player_board[i][j]), True, BLACK)
                WIN.blit(number, ((j+1)*50 + X_BUFFER, (i+1)*50))

            else:
                mistakes += 1
                pygame.draw.rect(WIN, INCORRECT_RED, ((j+1)*50, (i+1)*50, SMALL_BOX_WIDTH , SMALL_BOX_WIDTH ))
                if(SudokuSolver.player_board[i][j] != 0):
                    number = MYFONT.render(str(SudokuSolver.player_board[i][j]), True, PLAYER_COLOUR)
                    WIN.blit(number, ((j+1)*50 + X_BUFFER, (i+1)*50))
    if(mistakes == 0):
        winner_text = WINNER_FONT.render("YOU COMPLETED THE SUDOKU SUCESSFULLY!", True, BLACK)
        WIN.blit(winner_text, (50, 600))
    else:
        pygame.draw.rect(WIN, TAN, (0, 600, 550, 50))

def initialize():
    clear()
    SudokuSolver.create_player_board()
    SudokuSolver.solve()
    draw_base_numbers() 

def main():
    initialize()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                position = pygame.mouse.get_pos()
                if((50 <= position[0] <= 500) and (50 <= position[1] <= 500)):
                    value = current_box((position[0]//50, position[1]//50))
                    if value == "invalid_spot":
                        break
                    insert_number((position[0]//50, position[1]//50))
                elif((25 <= position[0] <= 180) and (525 <= position[1] <= 575)):
                    check()
                elif((200 <= position[0] <= 355) and (525 <= position[1] <= 575)):
                    solve()
                elif((375 <= position[0] <= 530) and (525 <= position[1] <= 575)):
                    pygame.draw.rect(WIN, TAN, (0, 600, 550, 50))
                    clear()
                elif((400 <= position[0] <= 500) and (5 <= position[1] <= 40)):
                    response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
                    SudokuSolver.board = response.json()['board']
                    initialize()

        draw_board()       
main()
