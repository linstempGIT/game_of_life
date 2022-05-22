from glob import glob
import pygame
import sys
from cell import Cell

clicking_cell = None
first_clicking_mode = None
continuous_mode = False
# living_cells_list用于标记被激活的cell的group_index
living_cells_list = []
'''
activable_dict用于标记可能在下一代被激活的cell,
键为在判断living_cells_list的livable时
其中的cell的env所提及的cell的group_index，
值为该group_index被提及数
（注意：可能包含了已被激活的点）
'''
activable_dict = {}
# auto_display为自动迭代判定变量
auto_display = False

def check_events(settings, cells_group):
    '''响应按键和鼠标事件'''

    for event in pygame.event.get():

        # 响应关闭窗口事件
        if event.type == pygame.QUIT:
            sys.exit()

        # 响应按键按下事件
        elif event.type == pygame.KEYDOWN:
            return reflect_keydown(settings, cells_group, event)

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
                reflect_moving_mouse(cells_group, mouse_pos)
            else:
                mouse_pos = pygame.mouse.get_pos()
                continuous_choise_cells(cells_group, mouse_pos)

        # 当鼠标点击时响应其松开鼠标事件
        elif clicking_cell and event.type == pygame.MOUSEBUTTONUP:
            reflect_up_mouse()

        # 当自动迭代为真时响应自定义事件，该事件将自动迭代cells_group
        elif auto_display and event.type == pygame.USEREVENT:
            enter_next_round(settings, cells_group)

    

def reflect_keydown(settings, cells_group, event):
    '''该函数对按键按下事件进行响应'''

    global continuous_mode

    # c键用以控制continuous_mode
    if event.key == pygame.K_c:
        continuous_mode = continuous_mode ^ True ^ False

    # r键用以重置cells_group所有cell，在按下键时进入选中模式
    elif event.key == pygame.K_r:
        reset_cells_group(cells_group, key_down=True)

    # n键用以进入当前cells_group状态的下一回合
    elif event.key == pygame.K_n:
        if living_cells_list:
            enter_next_round(settings, cells_group)

    # d键用以更改自动迭代判定变量
    elif event.key == pygame.K_d:
        global auto_display
        auto_display ^= True


def reflect_keyup(cells_group, event):
    '''该函数对按键松开事件进行响应'''

    # 重置cells_group，松开r键时重置
    if event.key == pygame.K_r:
        reset_cells_group(cells_group, key_down=False)


def reflect_clicking_cells(cells_group, mouse_pos):
    '''该函数响应鼠标点击单元格'''

    global clicking_cell
    global first_clicking_mode

    for cell in cells_group:
        if cell.rect.collidepoint(*mouse_pos):
            cell.change_mode(1)
            clicking_cell = cell
            first_clicking_mode = cell.mode


def continuous_choise_cells(cells_group,mouse_pos):
    '''该函数在点击鼠标后，对连续经过的单元格响应（continuous_mode)'''

    global clicking_cell
    global first_clicking_mode

    if not clicking_cell.rect.collidepoint(*mouse_pos):
        '''
        当移开选中单元格且鼠标未松开，判断该单元格与起始点击单元格模式是否一致,
        如果一致则进行模式改变，同时同步living_cells_list，否则还原
        '''
        if clicking_cell.mode == first_clicking_mode:
            manage_living_cells_list(clicking_cell.mode, clicking_cell.group_index)
            clicking_cell.change_mode(first_clicking_mode ^ 0 ^ 2)
        else:
            clicking_cell.change_mode(first_clicking_mode ^ 0 ^ 2)
        # 选中移动到的下一个单元格进行选中
        for cell in cells_group:
            if cell.rect.collidepoint(*mouse_pos):
                cell.change_mode(1)
                clicking_cell = cell


def reflect_moving_mouse(cells_group, mouse_pos):
    '''该函数在鼠标点击单元格时对其移动响应'''
    
    global first_clicking_mode

    if not clicking_cell.rect.collidepoint(*mouse_pos):
        # 当移开选中单元格且鼠标未松开,还原模式
        clicking_cell.change_mode(first_clicking_mode)
        # 对下移动到的下一个单元格进行选中
        reflect_clicking_cells(cells_group, mouse_pos)


def reflect_up_mouse():
    '''该函数在鼠标点击单元格后松开时响应'''

    global clicking_cell
    global first_clicking_mode
    
    # 连续模式下，松开鼠标的单元格应与首次选中单元格模式相同
    if continuous_mode:
        if clicking_cell.mode == first_clicking_mode:
            manage_living_cells_list(clicking_cell.mode, clicking_cell.group_index)
            clicking_cell.change_mode(first_clicking_mode ^ 0 ^ 2)
        else:
            clicking_cell.change_mode(first_clicking_mode ^ 0 ^ 2)
    # 非连续模式时同步living_cells_list并对松开鼠标的单元格模式进行取反
    else:
        manage_living_cells_list(clicking_cell.mode, clicking_cell.group_index)
        clicking_cell.change_mode(clicking_cell.mode ^ 2 ^ 0)
    # 消除clicking_cell和first_clicking_mode指向
    clicking_cell = None
    first_clicking_mode = None


def reset_cells_group(cells_group, key_down = True):
    '''该函数将cells_group内的所有cell重置'''

    if key_down:
        for cell in cells_group:
            cell.change_mode(1)
    else:
        for cell in cells_group:
            cell.change_mode(0)
    # 将living_cells_list清空
    living_cells_list.clear()


def manage_living_cells_list(before_mode, cell_group_index):
    '''该函数在改变单元格模式时同步living_cells_list'''

    if before_mode == 0:
        living_cells_list.append(cell_group_index)
    else:
        living_cells_list.remove(cell_group_index)


def copy_cells_group(settings, cells_group):
    '''
    对cells_group进行再创建copy法，返回再创建的cells_group_cp，
    尽量不要使用该函数，这会导致内存的剧烈增加
    '''

    cells_group_cp = []

    for cell in cells_group:
        cell_group_index = cell.group_index
        copy_cell = Cell(settings, cell_group_index)
        copy_cell.mode = cell.mode
        cells_group_cp.append(copy_cell)

    return cells_group_cp


def enter_next_round(settings, cells_group):
    '''
    该函数是进行cell迭代的函数，
    对满足生存条件的cell进行保留，
    对不满足生存条件的cell进行清除，
    对满足繁殖添加的cell进行激活
    '''

    # # 进行迭代处理时，进行操作的可变参数需进行copy，以保证参数不变
    # living_cells_list_cp = living_cells_list.copy()
    # cells_group_cp = copy_cells_group(settings, cells_group)

    # # 对未满足livable的cell进行清除，满足则保留
    # for group_index in living_cells_list_cp:
    #     if not judge_living_env(settings, cells_group_cp, group_index):
    #         cells_group[group_index].change_mode(0)
    #         living_cells_list.remove(group_index)

    # # 对activable_dict中的可被激活的cell进行激活，并清除activable_dict
    # # 先排除activable_dict中已被激活的cell
    # for group_index, count in activable_dict.items():
    #     if (group_index not in living_cells_list_cp) and\
    #         (count in settings.generable_nums):
    #         cells_group[group_index].change_mode(2)
    #         living_cells_list.append(group_index)
    # activable_dict.clear()

    '''
    重构：通过will_active_cells和will_deactive_cells来暂时存储
    需要清除和激活的cell的group_index，在完全判定好后，再改变
    living_cells_list和cells_group,而非通过copy来边判断边改变
    可变参数，导致空耗内存和性能
    '''

    will_active_cells = []
    will_deactive_cells = []

    for group_index in living_cells_list:
        if not judge_living_env(settings, cells_group, group_index):
            will_deactive_cells.append(group_index)

    for group_index, count in activable_dict.items():
        if (group_index not in living_cells_list) and\
        (count in settings.generable_nums):
            will_active_cells.append(group_index)

    for group_index in will_deactive_cells:
        cells_group[group_index].change_mode(0)
        living_cells_list.remove(group_index)

    for group_index in will_active_cells:
        cells_group[group_index].change_mode(2)
        living_cells_list.append(group_index)

    activable_dict.clear()


def judge_living_env(settings, cells_group, group_index):
    '''
    该函数对传入的env的生存条件进行判断,
    同时增加activable_dcit中关于env的cell的index的个数，
    如果该环境满足生存条件，返回True，否则返回False
    '''

    # 统计环境中的已激活cell数量
    env = cells_group[group_index].env
    exist_cells_num = 0
    for index in env:
        if index:
            activable_dict[index] = activable_dict.get(index,0) + 1
            if cells_group[index].mode == 2:
                exist_cells_num += 1
    
    if exist_cells_num in settings.livable_nums:

        return True

    return False





