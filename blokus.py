import pygame
import random

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 800
play_width = 600  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2  # top left x position of play area
top_left_y = s_height - (play_height + 100)  # top left y position of play area




def main_menu():

    grid = create_grid()
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Blokus')

    draw_grid(win,grid)



def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for _ in range(20)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def draw_grid(surface, grid):

    surface.fill((0, 0, 0))

    
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size),
                         (sx+play_width, sy + i*block_size))  # draws horizontal lines
        for j in range(len(grid[i]) + 1):
            pygame.draw.line(surface, (128, 128, 128), (sx + j *
                                                        block_size, sy), (sx+j*block_size, sy + play_height))

    pygame.draw.line(surface, (128, 128, 128), (sx, sy + len(grid)*block_size),
                         (sx+play_width, sy + len(grid)*block_size)) 

    pygame.display.update()


while True:
    main_menu()

