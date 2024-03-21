import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        # 初始化按钮的属性
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.buuton_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        # 调用函数，将要显示的字符串渲染为图像
        self._prep_msg(msg)

    # 将msg渲染为图像，并使其在按钮上居中
    def _prep_msg(self, msg):
        # font.render将存储在msg中的文本转换为图像，第二个参数指定是否要反锯齿功能 三四表示文本颜色，背景色
        self.msg_image = self.font.render(msg, True,
                                          self.text_color, self.buuton_color)
        # 让文本图像在按钮上居中
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制表示按钮的矩形
        self.screen.fill(self.buuton_color, self.rect)
        # 传递一副图像及相关的rect
        self.screen.blit(self.msg_image, self.msg_image_rect)
