import pygame
import random
import math


''' GLOBALS VARS '''

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


blocks = [None] * 42
block_rectangles = [[None for _ in range(48)] for _ in range(26)]

offset_grid = [[[0,0] for _ in range(48)] for _ in range(26)]
locked_positions = {}


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

''' Initializes the initital rectangles in the grid'''

def create_rectangles(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
                block_rectangles[i][j] = (pygame.Rect(j*block_size,
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
    Draws the grid and colors 
    each rectangle in accordance to the color in each key of grid.
    '''

    for i in range(len(grid)):
        for j in range(len(grid[i])):

                if grid[i][j] != (0,0,0):
                    pygame.draw.rect(surface, grid[i][j], (j*block_size + offset_grid[i][j][0],
                                                        i*block_size + offset_grid[i][j][1], block_size, block_size), 0)
                                                    

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

    pygame.font.init()
    win = pygame.display.set_mode((s_width, s_height))
    running = True
    grid = create_grid(win)
    create_rectangles(grid)
    pygame.display.set_caption('Blokus')
    down  = False
    valid_drag = False

    ''' Factors that change the block while on drag on drop '''
    
    collided_rects = []
    rect_positions = []
    gx = 0
    gy = 0
    offset_x = 0
    offset_y = 0
    rect_x = 0
    rect_y = 0
    block_index = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    print("Mouse Down")
                    down = True
                    
                    ''' Goes over the rectangles list to figure which block the user is about to drag
                        (x,y (index) of the grid)
                    '''

                    for i in range(len(block_rectangles)):
                        for j in range(len(block_rectangles[i])):
                            rect = block_rectangles[i][j]
                            if rect.collidepoint(event.pos):
                                collided_rects.append(rect)
                                rect_x = rect.x
                                rect_y = rect.y
                                
                                gx = int(rect.x/block_size)
                                gy = int(rect.y/block_size)

                                if grid[gy][gx] != (0,0,0):
                                    valid_drag = True


            elif event.type == pygame.MOUSEBUTTONUP:
                print("Mouse Up")

                if valid_drag and down:

                    ''' Changes the new default x,y coordinate of the block object'''

                    for i in range(len(block_rectangles)):
                        for j in range(len(block_rectangles[i])):
                            rect = block_rectangles[i][j]
                            if rect.collidepoint(event.pos):
                                collided_rects.append(rect)
                                
                                new_gx = int(rect.x/block_size)
                                new_gy = int(rect.y/block_size)
                                
                                print('Block coordinates')
                                print(blocks[block_index].x, blocks[block_index].y)
                                print('Old coordinates')
                                print(gx,gy)

                                print('New coordinates')
                                print(new_gx, new_gy)

                    b = blocks[block_index]
                    shape_pos = convert_shape_format(b.x,b.y,b.shape[0])
        
                    ''' 
                        Resets the previous location of block.
                        Makes the grid coordinates black in color.
                    '''
                    for i in range(len(shape_pos)):
                        (x,y) = shape_pos[i]
                        grid[y][x] = (0,0,0)

                    '''
                        Updates the default positions of the block object.
                    '''

                    print(block_index)
                    if block_index<21:
                        default_shape_positions_player1[block_index][0] += new_gx - gx
                        default_shape_positions_player1[block_index][1] += new_gy - gy
                    
                    elif block_index>=21:
                        default_shape_positions_player2[block_index-21][0] += new_gx - gx
                        default_shape_positions_player2[block_index-21][1] += new_gy - gy

                    '''
                        Resets to offset grid to 0 since it is no longer needed.
                        Rest everything to base case. 
                    '''
                    for (a,b) in blocks[block_index].positions:
                        offset_grid[b][a][0] = 0
                        offset_grid[b][a][1] = 0
                    
                        collided_rects = []

                        rect_positions = []

                        gx = 0
                        gy = 0
                        offset_x = 0
                        offset_y = 0

                        rect_x = 0
                        rect_y = 0

                        block_index = 0

                    down = False
                    valid_drag = False

  
            elif event.type == pygame.MOUSEMOTION:
                if down and valid_drag: 
                    print("Mouse Drag") 

                    ''' Uses the grid index to add an offset to every rectangle 
                    in the block while drag'''

                    offset_x = event.pos[0] - rect_x
                    offset_y = event.pos[1] - rect_y

                    offset_grid[gy][gx][0] = offset_x
                    offset_grid[gy][gx][1] = offset_y

                    for block in blocks:
                        if (gx,gy) in block.positions:
                            block_index = blocks.index(block)
                            for (a,b) in block.positions:
                                rect_positions.append((a,b))
                                offset_grid[b][a][0] = offset_x
                                offset_grid[b][a][1] = offset_y

                            
        for i in range(21):
            current_piece = Block(default_shape_positions_player1[i][0],default_shape_positions_player1[i][1], shapes[i],(237,41,57))
            blocks[i] = current_piece

            shape_pos = convert_shape_format(current_piece.x,current_piece.y,current_piece.shape[0])
    
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]
                    grid[y][x] = current_piece.color
        
        for i in range(21):
            current_piece = Block(default_shape_positions_player2[i][0],default_shape_positions_player2[i][1], shapes[i], (0,0,255))
            blocks[i+21] = current_piece

            shape_pos = convert_shape_format(current_piece.x,current_piece.y,current_piece.shape[0])
            for i in range(len(shape_pos)):
                    (x,y) = shape_pos[i]

                    grid[y][x] = current_piece.color

        draw_grid(win,grid)


main_menu()

