import pygame
from settings import Settings
from pygame.sprite import Group
from cell import Cell

def initialize():
    '''该函数初始化屏幕'''

    # 初始pygame，字体，设置和屏幕
    pygame.init()
    pygame.font.init()
    settings = Settings()
    screen = pygame.display.set_mode(settings.screen_size)
    #screen.fill(settings.screen_bg_color)
    pygame.display.set_caption("Life Game")

    return screen

def get_cells_params(settings):
    '''根据settings的参数返回cell的排列参数列表'''

    screen_width = settings.screen_size[0]
    screen_heigth = settings.screen_size[1]
    cell_width = settings.cell_size[0]
    cell_height = settings.cell_size[1]

    # 计算每行和每列可生成的cell个数
    x_cell_nums = screen_width // cell_width
    y_cell_nums = screen_heigth // cell_height

    # 返回每个可生成的cell的x，y所构成的列表
    cells_coordinates = []
    for index_x in range(x_cell_nums):
        for index_y in range(y_cell_nums):
            coordinate = (index_x * cell_width, index_y * cell_height)
            cells_coordinates.append(coordinate)
    
    return cells_coordinates

def init_cells_group(settings):
    '''该函数创建并返回管理cell的编组'''

    cells_group = Group()
    for x, y in get_cells_params(settings):
        cell = Cell(settings, x, y)
        cells_group.add(cell)
        
    return cells_group

def display_cells_group(screen, cells_group):
    '''该函数将cells_group编组里的cell渲染到screen'''
    
    cells_group.draw(screen)

def display_screen(screen, cells_group):
    '''该函数将screen上的图像展示'''

    display_cells_group(screen, cells_group)
    pygame.display.flip()