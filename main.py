import pygame
import display_functions as df
import game_functions as gf
from settings import Settings

def run_game():
    '''程序入口'''
    
    # 载入相关设置Settings类
    settings = Settings()
    # 初始化屏幕、字体和设置，返回屏幕引用
    screen = df.initialize()
    # 创建cell的编组
    cells_group = df.init_cells_group(settings)
    # 创建自动迭代定时触发器
    pygame.time.set_timer(pygame.USEREVENT, settings.auto_display_speed)

    # 开始游戏循环
    while True:

        # 检查标准输入并响应
        gf.check_events(settings, cells_group)

        # 渲染screen图像
        df.display_screen(screen, cells_group)




run_game() 
