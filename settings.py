class Settings:
    # 存储游戏中所有的类
    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 0.5
        self.ship_limit = 3

        # 子弹设置 宽3像素 高15像素
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # 外星人设置
        self.alien_speed = 0.8
        # 外星人向下移动的速度
        self.fleet_drop_speed = 5
        # 加快游戏节奏
        self.speedup_scale = 1.1
        # 外星人分数提高
        self.score_scale = 1.5
        # fleet_direction为1表示向右移动 -1表示向左移动
        self.fleet_direction = 1

    # 初始化随着游戏进行而变化的位置
    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.8
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    # 提高速度设置
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
