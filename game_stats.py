class GameStats:
    def __init__(self, ai_game):
        # 初始化统计信息
        self.settings = ai_game.settings
        self.reset_stats()
        # 添加一个作为标志的属性game_active,玩家飞船用完后结束游戏
        self.game_active = False
        # 任何情况下都不应重置最高分
        self.high_score = 0  # 最高分
        self.level = 1  # 玩家等级

    def reset_stats(self):
        # 初始化在游戏期间可能变化的统计信息
        self.ship_left = self.settings.ship_limit
        self.score = 0
