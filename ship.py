import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        # 初始化飞船并设置并初始化其位置
        # 将屏幕赋给了飞船的一个属性
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # get_rect方法访问屏幕的属性rect
        self.screen_rect = ai_game.screen.get_rect()

        # pygame.image.load加载图像，函数返回一个表示飞船的surface
        self.image = pygame.image.load('imgs/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x中存储小数值 调整飞船位置时，将增减一个单位为像素的小数值
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    # 根据移动标志移动飞船位置
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.x += 1
            # 更新飞船而不是rect对象的x值
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1
            self.x -= self.settings.ship_speed
        # self.rect.x只存储self.x的整数部分
        self.rect.x = self.x

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # 让飞船在屏幕居中显示
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
