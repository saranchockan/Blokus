''' Make the whole screen a grid. Determine the play grid by checking if a point is inside the border rectangle.  '''

import pygame
import random
import block

pygame.font.init()

# GLOBALS VARS
s_width = 1440
s_height = 800
play_width = 600  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2  # top left x position of play area
top_left_y = s_height - (play_height + 100)  # top left y position of play area

play_border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)
S = [['.....',
    '......',
    '..00..',
    '.00...',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]
shapes = [S, Z, I, O, J, L, T]

shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255),
                    (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Block(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

    
''' Returns a random block object '''

def get_shape():  
    return Block(5, 0, random.choice(shapes))


def convert_shape_format(shape):
    positions = []
    '''
    Rotation determines the current position/format of the block
    '''
    format = shape.shape[shape.rotation % len(shape.shape)]

    '''
    Loops through every row of the current shape format 
    for determining the shape based off '.' & '0'

    '''
    for i, line in enumerate(format):
            '''
            current line in the shape format. For example 
            a line a would be: '...0...' and each character would be a column
            '''

            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                        positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # test this offset
    
    print(positions)

    return positions


''' Creates the matrix 'grid' that consists of hex colors '''

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

    '''
    pygame.draw.rect()
    draw a rectangle shape
    rect(Surface, color, Rect, width=0) -> Rect

    -----  Rect argument is (x,y,width, height)

    The below function draws the grid and colors 
    each rectangle in accordance to the color in each key of grid.
    '''

    for i in range(len(grid)):
        for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size,
                                                    top_left_y + i*block_size, block_size, block_size), 0)

    ''' Draws a rectangle the red border '''
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                                            top_left_y, play_width, play_height), 4)


    ''' Draws the line for the rectangles on the grid '''

    for i in range(len(grid)):
        ''' draws horizontal lines '''
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*block_size),
                         (sx+play_width, sy + i*block_size))  
        for j in range(len(grid[i]) + 1):
            pygame.draw.line(surface, (128, 128, 128), (sx + j *
                                                        block_size, sy), (sx+j*block_size, sy + play_height))

    ''' Draws the last vertical line of the grid '''

    pygame.draw.line(surface, (128, 128, 128), (sx, sy + len(grid)*block_size),
                         (sx+play_width, sy + len(grid)*block_size)) 

    pygame.display.update()



def main_menu():
    grid = create_grid()
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Blokus')
    draw_grid(win,grid)

while True:
    main_menu()

