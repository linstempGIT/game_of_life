from pydoc import cli
import pygame
import sys
from cell import Cell

clicking_cell = None
continuous_mode = False

def check_events(screen, cells_group):
    '''响应按键和鼠标事件'''

    for event in pygame.event.get():

        # 响应关闭窗口事件
        if event.type == pygame.QUIT:
            sys.exit()

        # 响应按键按下事件
        elif event.type == pygame.KEYDOWN:
            reflect_keydown(cells_group, event)

        # 响应松开按键事件
        elif event.type == pygame.KEYUP:
            reflect_keyup(cells_group, event)

        # 响应鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            reflect_clicking_cells(cells_group, mouse_pos)

        # 当鼠标点击时响应其移动事件
        elif clicking_cell and event.type == pygame.MOUSEMOTION:
            if continuous_mode == False:
                mouse_pos = pygame.mouse.get_pos()
                reflect_moving_mouse(mouse_pos)
            else:
                mouse_pos = pygame.mouse.get_pos()
                continuous_choise_cells(cells_group, mouse_pos)

        # 当鼠标点击时响应其松开鼠标事件
        elif clicking_cell and event.type == pygame.MOUSEBUTTONUP:
            reflect_up_mouse()


def reflect_keydown(cells_group, event):
    '''该函数对按键按下事件进行响应'''

    global continuous_mode

    # c键用以控制continuous_mode
    if event.key == pygame.K_c:
        continuous_mode = continuous_mode ^ True ^ False

    # r键用以重置cells_group所有cell，在按下键时进入选中模式
    elif event.key == pygame.K_r:
        reset_cells_group(cells_group, key_down=True)


def reflect_keyup(cells_group, event):
    '''该函数对按键松开事件进行响应'''

    # 重置cells_group，松开r键时重置
    if event.key == pygame.K_r:
        reset_cells_group(cells_group, key_down=False)


def reflect_clicking_cells(cells_group, mouse_pos):
    '''该函数响应鼠标点击单元格'''

    global clicking_cell

    for cell in cells_group:
        if cell.rect.collidepoint(*mouse_pos):
            cell.change_mode(1)
            clicking_cell = cell


def continuous_choise_cells(cell_groups,mouse_pos):
    '''该函数在点击鼠标后，对连续经过的单元格响应（continuous_mode)'''

    if not clicking_cell.rect.collidepoint(*mouse_pos):
        # 当移开选中单元格且鼠标未松开，单元格模式取反
        clicking_cell.change_mode(clicking_cell.mode ^ 2 ^ 0)
        # 对下移动到的下一个单元格进行选中
        reflect_clicking_cells(cell_groups, mouse_pos)


def reflect_moving_mouse(mouse_pos):
    '''该函数在鼠标点击单元格时对其移动响应'''
    
    global clicking_cell

    if not clicking_cell.rect.collidepoint(*mouse_pos):
        clicking_cell.change_mode(clicking_cell.mode)
        clicking_cell = None


def reflect_up_mouse():
    '''该函数在鼠标点击单元格后松开时响应'''

    global clicking_cell
    
    if clicking_cell.mode == 0:
        clicking_cell.change_mode(2)
    elif clicking_cell.mode == 2:
        clicking_cell.change_mode(0)
    clicking_cell = None


def reset_cells_group(cells_group, key_down = True):
    '''该函数将cells_group内的所有cell重置'''

    if key_down:
        for cell in cells_group:
            cell.change_mode(1)
    else:
        for cell in cells_group:
            cell.change_mode(0)
