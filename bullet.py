import pygame
from pygame.sprite import Sprite


# 通过使用精灵（sprite），可将游戏中相关的元素编组，进而同时操作所有的元素

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 子弹不是图像，因此用Rect类从头开始建一个矩形 参数为：矩形左上角的x，y坐标，宽，高
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    # 向上移动子弹
    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    # 在屏幕上绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
