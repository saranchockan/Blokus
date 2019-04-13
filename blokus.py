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

block_rectangles = []

blocks = [None] * 42

offset_grid = [[[0,0] for _ in range(48)] for _ in range(26)]


class Block(object):
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0
        self.positions = convert_shape_format(x,y,shape[0])


def convert_shape_format(x, y, format):
    positions = []
    '''
    Rotation determines the current position/format of the block
    '''

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
                        positions.append((x + j, y + i))
    
    for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # test this offset
    
    
    return positions

def create_rectangles(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
                block_rectangles.append(pygame.Rect(j*block_size,
                                                    i*block_size, block_size, block_size))


''' Creates the matrix 'grid' that consists of hex colors '''

def create_grid(surface, locked_positions = {}):

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
    ''' Draws the blocks '''
    for i in range(len(grid)):
        for j in range(len(grid[i])):

                if grid[i][j] != (0,0,0):
                    pygame.draw.rect(surface, grid[i][j], (j*block_size + offset_grid[i][j][0],
                                                        i*block_size + offset_grid[i][j][1], block_size, block_size), 0)

                    block_rectangles[i+j] = pygame.Rect(j*block_size + offset_grid[i][j][0],
                                                        i*block_size + offset_grid[i][j][1], block_size, block_size)
                                                    

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
    win = pygame.display.set_mode((s_width, s_height))
    running = True
    grid = create_grid(win)
    create_rectangles(grid)
    pygame.display.set_caption('Blokus')
    down  = False
    valid_drag = False

    gx = 0
    gy = 0
    offset_x = 0
    offset_y = 0

    rect_x = 0
    rect_y = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    print("Mouse Down")
                    down = True
                    for rect in block_rectangles:
                        if rect.collidepoint(event.pos):
                            #print(rect.x)
                            rect_x = rect.x
                            rect_y = rect.y
                            
                            gx = int(rect.x/block_size)
                            gy = int(rect.y/block_size)
                            
                            if grid[gy][gx] != (0,0,0):
                                valid_drag = True
                            '''
                            if grid[gy][gx] != (0,0,0):
                                valid_drag = True

                                offset_x = event.pos[0] - rect.x
                                offset_y = event.pos[1] - rect.y

                                # print(offset_x,offset_y)

                                offset_grid[gy][gx][0] = offset_x
                                offset_grid[gy][gx][1] = offset_y
                                #print(event.pos)  

                                for block in blocks:
                                    if (gx,gy) in block.positions:
                                        print("Fuck")
                                        print(gx,gy)
                                        print(block.positions)
                                        for (a,b) in block.positions:
                                            # print(offset_x,offset_y)
                                            offset_grid[b][a][0] = offset_x
                                            offset_grid[b][a][1] = offset_y
                            '''


            elif event.type == pygame.MOUSEBUTTONUP:
                down = False
                valid_drag = False
                print("Mouse Up")

            elif event.type == pygame.MOUSEMOTION:
                if down and valid_drag: 
                    print("Mouse Drag") 
                    offset_x = event.pos[0] - rect_x
                    offset_y = event.pos[1] - rect_y

                    # print(offset_x,offset_y)

                    offset_grid[gy][gx][0] = offset_x
                    offset_grid[gy][gx][1] = offset_y

                    for block in blocks:
                        if (gx,gy) in block.positions:
                            print("Fuck")
                            print(gx,gy)
                            print(block.positions)
                            for (a,b) in block.positions:
                                # print(offset_x,offset_y)
                                offset_grid[b][a][0] = offset_x
                                offset_grid[b][a][1] = offset_y
                    '''
                    for i in range(len(offset_grid)):
                        for j in range(len(offset_grid[i])):
                            if offset_grid[i][j] != [0,0]:
                                print(offset_grid[i][j])
                    '''
                    


        
        for i in range(21):
            current_piece = Block(default_shape_positions_player1[i][0],default_shape_positions_player1[i][1], shapes[i],(237,41,57))
            blocks[i] = current_piece

            shape_pos = convert_shape_format(current_piece.x,current_piece.y,current_piece.shape[0])
    
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]

                    grid[math.floor(y)][math.floor(x)] = current_piece.color
        
        for i in range(21):
            current_piece = Block(default_shape_positions_player2[i][0],default_shape_positions_player2[i][1], shapes[i], (0,0,255))
            blocks[i+21] = current_piece

            shape_pos = convert_shape_format(current_piece.x,current_piece.y,current_piece.shape[0])
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]

                    grid[y][x] = current_piece.color

        draw_grid(win,grid)


main_menu()

