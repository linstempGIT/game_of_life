class Settings():
    '''存储游戏中的设置参数'''

    def __init__(self) -> None:
        '''初始化游戏设置'''

        # 屏幕设置
        self.screen_size = (800, 800)
        self.screen_bg_color = (230, 230, 230)

        # 自动播放速度设置
        self.auto_display_speed = 1000
        
        # 单元格设置
        self.cell_size = (20, 20)
        # x_cell_nums表示在屏幕的横向可生成的最大cell个数
        self.x_cell_params = divmod(self.screen_size[0], self.cell_size[0])
        self.x_cell_nums = self.x_cell_params[0]
        # x_cell_begin表示横向的cell生成的起始位置
        self.x_cell_begin = self.x_cell_params[1] // 2
        # y_cell_nums表示在屏幕的纵向可生成的最大cell个数
        self.y_cell_params = divmod(self.screen_size[1], self.cell_size[1])
        self.y_cell_nums = self.y_cell_params[0]
        # y_cell_begin表示纵向的cell生成的起始位置
        self.y_cell_begin = self.y_cell_params[1] // 2
        # cell_nums表示在给定的屏幕和cell参数时能创建的最多cell数
        self.cell_nums = self.x_cell_nums * self.y_cell_nums
        
        # 游戏规则设置
        self.livable_nums = (2, 3)
        self.unlivable_nums = (0, 1, 4, 5, 6, 7, 8)
        self.generable_nums = (3,)