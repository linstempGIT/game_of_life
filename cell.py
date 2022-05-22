from copy import deepcopy
from settings import Settings
import pygame
from os.path import dirname

dir_name = dirname(__file__) + '/images/'

class Cell():
    '''存储cell类的属性和方法'''

    def __init__(self, settings, group_index):
        '''初始化单元格，并设置其起始位置'''

        super().__init__()

        # 设置cell的大小
        self.cell_size = settings.cell_size

        # 加载cell的未激活模式图像，并为其创建一个rect对象
        self.origin_image_0 = pygame.image.load(dir_name + 'cell_image_0.png')
        self.image_0 = self.change_size(self.origin_image_0)

        # 加载cell的选中模式图像，为其创建一个rect对象
        self.origin_image_1 = pygame.image.load(dir_name + 'cell_image_1.png')
        self.image_1 = self.change_size(self.origin_image_1)

        # 加载cell的激活模式的图像，并为其创建一个rect对象
        self.origin_image_2 = pygame.image.load(dir_name + 'cell_image_2.png')
        self.image_2 = self.change_size(self.origin_image_2)

        # 创建cell时，默认主图像为未激活模式
        self.mode = 0
        self.image = self.image_0
        self.rect = self.image.get_rect()

        # 根据group中的index和settings的相关参数确定cell在屏幕上的位置
        self.group_index = group_index
        self.y_index, self.x_index = divmod(self.group_index, settings.x_cell_nums)
        self.rect.x = settings.x_cell_begin + self.cell_size[0] * self.x_index
        self.rect.y = settings.y_cell_begin + self.cell_size[1] * self.y_index

        # 根据cell的位置信息，获得它的env中的cell的index
        self.get_env(settings)
        self.env = (self.n_index, self.s_index, self.w_index, self.e_index,
                    self.nw_index, self.ne_index, self.sw_index, self.se_index)
        

    def change_size(self, image):
        '''该方法将传入的image设置为cell_size，并返回'''

        return pygame.transform.scale(image, (self.cell_size))


    def change_mode(self, mode=0):
        '''该方法改变主图像为指定的模式(未指定模式默认为0）'''

        if mode == 1:
            self.image = self.image_1
        elif mode == 2:
            self.mode = 2
            self.image = self.image_2
        else:
            self.mode = 0
            self.image = self.image_0


    def get_env(self, settings):
        '''该方法根据自身的位置信息的相关参数获得env的cell的index'''

        # 获得north和south方向的cell的index，如果是边界则为None
        self.n_index = self.group_index - settings.x_cell_nums
        self.s_index = self.group_index + settings.x_cell_nums
        if self.y_index == 0:
            self.n_index = None
        if self.y_index == (settings.y_cell_nums - 1) :
            self.s_index = None

        # 获得west和east方向的cell的index，如果是边界则为None
        self.w_index = self.group_index - 1
        self.e_index = self.group_index + 1
        if self.x_index == 0:
            self.w_index = None
        if self.x_index == (settings.x_cell_nums -1):
            self.e_index = None

        # 获得northwest和northeast方向的cell的index，如果是边界则为None
        if self.n_index:
            if self.w_index:
                self.nw_index = self.n_index - 1
            else:
                self.nw_index = None
            if self.e_index:
                self.ne_index = self.n_index + 1
            else:
                self.ne_index = None
        else:
            self.nw_index = None
            self.ne_index = None

        # 获得southwest和southeast方向的cell的index，如果是边界则为None
        if self.s_index:
            if self.w_index:
                self.sw_index = self.s_index - 1
            else:
                self.sw_index = None
            if self.e_index:
                self.se_index = self.s_index + 1
            else:
                self.se_index = None
        else:
            self.sw_index = None
            self.se_index = None


# cell模块测试
if __name__ == '__main__':
    settings = Settings()
    example_cell = Cell(settings, 0)