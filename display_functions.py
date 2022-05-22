from tkinter import image_names
import pygame
from game_functions import enter_next_round
from os.path import dirname
from settings import Settings
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


'''对cell进行重构，通过settings和group_index自行判断coordinate'''
# def get_cells_params(settings):
#     '''根据settings的参数返回cell的排列参数列表'''

#     screen_width = settings.screen_size[0]
#     screen_heigth = settings.screen_size[1]
#     cell_width = settings.cell_size[0]
#     cell_height = settings.cell_size[1]

#     # 计算每行和每列可生成的cell个数
#     x_cell_nums = screen_width // cell_width
#     y_cell_nums = screen_heigth // cell_height

#     # 返回每个可生成的cell的x，y所构成的列表
#     cells_coordinates = []
#     for index_x in range(x_cell_nums):
#         for index_y in range(y_cell_nums):
#             coordinate = (index_x * cell_width, index_y * cell_height)
#             cells_coordinates.append(coordinate)
    
#     return cells_coordinates

def init_cells_image(settings):
    '''该函数导入并创建单元格所需要的图像'''

    image_size = settings.cell_size
    dir_name = dirname(__file__) + '/images/'
    images_name = [dir_name + 'cell_image_' + str(i) + '.png' for i in range(3)]

    origin_images = tuple(map(pygame.image.load, images_name))
    size_list = [image_size] * 3

    return tuple(map(pygame.transform.scale, origin_images, size_list))


def init_cells_group(settings):
    '''该函数创建并返回管理cell的编组'''

    cells_group = []
    for group_index in range(settings.cell_nums):
        images = init_cells_image(settings)
        cell = Cell(settings, group_index, images)
        cells_group.append(cell)
        
    return cells_group


def display_cells_group(screen, cells_group):
    '''该函数将cells_group编组里的cell渲染到screen'''
    
    for cell in cells_group:
        screen.blit(cell.image, cell.rect)


def display_screen(screen, cells_group):
    '''该函数将screen上的图像展示'''

    display_cells_group(screen, cells_group)
    pygame.display.flip()