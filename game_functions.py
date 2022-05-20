import pygame
import sys
from cell import Cell

# click_define = False

def check_events(screen, cells_group):
    '''响应按键和鼠标事件'''

    clicking_cell = None

    for event in pygame.event.get():

        # 响应关闭窗口事件
        if event.type == pygame.QUIT:
            sys.exit()

        # 响应鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicking_cell = reflect_clicking_cells(cells_group, mouse_pos)

        # 当鼠标点击后响应其移动事件
        elif clicking_cell and event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            reflect_moving_mouse()

def reflect_clicking_cells(cells_group, mouse_pos):
    '''该函数响应鼠标点击单元格'''

    for cell in cells_group:
        if cell.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            cell.change_mode(1)

            return cell

def reflect_moving_mouse(clicking_cell, mouse_pos):
    '''该函数在鼠标点击单元格时对其移动响应'''

    if not clicking_cell.rect
