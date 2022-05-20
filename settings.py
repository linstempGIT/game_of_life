class Settings():
    '''存储游戏中的设置参数'''

    def __init__(self) -> None:
        '''初始化游戏设置'''

        # 屏幕设置
        self.screen_size = (800, 800)
        self.screen_bg_color = (230, 230, 230)

        # 单元格设置
        self.cell_size = (20, 20)
        