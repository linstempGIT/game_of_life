import pygame
from pygame.sprite import Sprite
from os.path import dirname

dir_name = dirname(__file__) + '/'

class Cell(Sprite):
    '''存储cell类的属性和方法'''

    def __init__(self, settings, x=0, y=0):
        '''初始化单元格，并设置其起始位置'''

        super().__init__()

        # 设置cell的大小
        self.cell_size = settings.cell_size

        # 加载cell的未激活模式图像，并为其创建一个rect对象
        self.image_0 = self.change_size(pygame.image
                                            .load(dir_name + 'cell_image_0.png'))

        # 加载cell的选中模式图像，为其创建一个rect对象
        self.image_1 = self.change_size(pygame.image
                                            .load(dir_name + 'cell_image_1.png'))

        # 加载cell的激活模式的图像，并为其创建一个rect对象
        self.image_2 = self.change_size(pygame.image
                                            .load(dir_name + 'cell_image_2.png'))

        # 创建cell时，默认主图像为未激活模式
        self.mode = 0
        self.image = self.image_0
        self.rect = self.image.get_rect()

        # 确定cell在屏幕上的位置（默认为0，0）
        self.rect.x = x
        self.rect.y = y
        
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