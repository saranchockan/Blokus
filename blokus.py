''' Make the whole screen a grid. Determine the play grid by checking if a point is inside the border rectangle.  '''

import pygame
import random
import math

pygame.font.init()

# GLOBALS VARS
s_width = 1440
s_height = 780
play_width = 600  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2  # top left x position of play area
top_left_y = s_height - (play_height + 90)  # top left y position of play area

play_border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)

shapes = [[['.....',
    '......',
    '..00..',
    '.00...',
    '.....']],

    [['.....',
    '......',
    '..000.',
    '.00...',
    '.....']],

    [['.....',
    '.000.',
    '.....',
    '.....',
    '.....']],

    [['.....',
    '.0000',
    '.....',
    '.....',
    '.....']],

    [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']],

    [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....']],

    [['.....',
    '.0...',
    '.0000',
    '.....',
    '.....']],

    [['.0...',
    '.0...',
    '.000.',
    '.....',
    '.....']],

    [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '..0..']],

    [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....']],

    [['..0..',
    '..0..',
    '.000.',
    '.....',
    '.....']],

    [['.....',
    '.0...',
    '.00..',
    '.00..',
    '.....']],

    [['.....',
    '..0..',
    '.000.',
    '..0..',
    '.....']],

    [['.....',
    '.....',
    '..00.',
    '...0.',
    '.....']],

    [['0....',
    '.....',
    '.....',
    '.....',
    '.....']],

    [['00...',
    '.....',
    '.....',
    '.....',
    '.....']],

    [['.....',
    '..00.',
    '.00..',
    '..0..',
    '.....']],

    [['.....',
    '..00.',
    '..0..',
    '..00.',
    '.....']],

    [['.....',
      '..00.',
      '.00..',
      '.0...',
      '.....']],
    [['.....',
      '...0.',
      '.000.',
      '.0...',
      '.....']],

    [['.0...',
      '0000.',
      '.....',
      '.....',
      '.....']]
    ]

default_shape_positions_player1 = [[2,3], [6,3], [11,4], 
                          [2,7], [7,6],[11,6],
                          [2,9],[7,11],[11,10],
                          [2,12],[7,15],[11,15],
                          [2,15],[5,17],[10,19],
                          [3,20],[7,21],[10,19],
                          [2,22],[6,25],[11,25]]

default_shape_positions_player2 = [[36,3], [40,3], [45,4], 
                          [36,7], [41,6],[45,6],
                          [36,9],[41,11],[45,10],
                          [36,12],[41,15],[45,15],
                          [36,15],[39,17],[44,19],
                          [37,20],[41,21],[44,19],
                          [36,22],[40,25],[45,25]]
                  
class Block(object):
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    
''' Returns a random block object '''

def get_shape():  
    return Block(10, 10, random.choice(shapes))


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
            format = shape.shape[shape.rotation % len(shape.shape)]

            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                        positions.append((shape.x + j, shape.y + i))
    
    for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # test this offset
    
    
    return positions



''' Creates the matrix 'grid' that consists of hex colors '''

def create_grid(locked_positions = {}):

    grid = [[(0, 0, 0) for _ in range(48)] for _ in range(26)]

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
                pygame.draw.rect(surface, grid[i][j], (j*block_size,
                                                    i*block_size, block_size, block_size), 0)

    ''' Draws a rectangle the red border '''
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x,
                                            top_left_y, play_width, play_height), 4)


    ''' Draws the line for the rectangles on the grid '''

    for i in range(len(grid)):
        ''' draws horizontal lines '''
        pygame.draw.line(surface, (128, 128, 128), (0, i*block_size),
                         (1440, i*block_size))
                        
        for j in range(len(grid[i]) + 1):
            pygame.draw.line(surface, (128, 128, 128), (j *
                                                        block_size, 0), (j*block_size, 780))

    ''' Draws the last vertical line of the grid '''

    pygame.draw.line(surface, (128, 128, 128), (sx, sy + len(grid)*block_size),
                         (sx+play_width, sy + len(grid)*block_size)) 

    ''' Draws the neon grid for the play area '''

    for i in range(20):
        ''' Draws the horizontal lines of the grid '''
        pygame.draw.line(surface, (153, 255, 51), (sx, sy + i*block_size),
                         (sx+play_width, sy+ i*block_size))
        for j in range(21):
            pygame.draw.line(surface, (153, 255, 51), (sx + j *
                                                        block_size, sy), (sx + j*block_size, sy + play_height))

    pygame.display.update()



def main_menu():

    running = True
    grid = create_grid()
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Blokus')

    down  = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    print("Mouse Down")
                    down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                down = False
                print("Mouse Up")

            elif event.type == pygame.MOUSEMOTION:
                if down: 
                    print("Mouse Drag")             
        
        for i in range(21):
            current_piece = Block(default_shape_positions_player1[i][0],default_shape_positions_player1[i][1], shapes[i],(237,41,57))

            shape_pos = convert_shape_format(current_piece)
    
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]

                    grid[math.floor(y)][math.floor(x)] = current_piece.color
        
        for i in range(21):
            current_piece = Block(default_shape_positions_player2[i][0],default_shape_positions_player2[i][1], shapes[i], (0,0,255))

            shape_pos = convert_shape_format(current_piece)
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]

                    grid[y][x] = current_piece.color

        draw_grid(win,grid)


main_menu()

