import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        # 初始化游戏并创建游戏环境
        pygame.display.set_caption("Alien Invasion")

        # self.screen = pygame.display.set_mode((1200, 800))
        # # 设置背景颜色
        # self.bg_color = (230, 230, 230)

        # 将代码换成创建setting实例
        self.settings = Settings()
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height)
        # )
        # 让pygame生成一个覆盖整个显示器的屏幕
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 创建记分牌
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        # 创建一个编组 用于存储所有有效子弹
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建按钮
        self.play_button = Button(self, "play")

    def run_game(self):
        # 开始游戏主循环
        while True:
            # 任何时候都要调用_check_events, 检测玩家行为
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    # 监视键盘和鼠标事件
    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 用鼠标点击play按钮
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # mouse.get_pos返回一个元组，其中包含玩家点击时的x坐标和y坐标
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            # 响应按下按键
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # 响应松开按键
            elif event.type == pygame.KEYUP:
                self._check_updown_events(event)

    # 让玩家点击play按钮时开始新游戏
    # 使用rect的collidepoint方法检查鼠标单击位置是否在play按钮内
    def _check_play_button(self, mouse_pos):
        # button_clicked值为true或false
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()  # 重置游戏信息
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人并让飞船居中
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        # 每次循环时都重新绘制屏幕 即更新屏幕上的图像 并切换到新图像
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    # 响应按键
    def _check_keydown_events(self, event):
        # 按下为右箭头
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        # 按下为左箭头
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    # 响应松开
    def _check_updown_events(self, event):
        # 松开右箭头
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        # 松开左箭头
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # 创建一颗子弹,加入到编组bullets中
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # 更新子弹的位置
        self.bullets.update()
        # 删除消失的子弹 否则占用内存
        # 不能从for循环遍历的列表或编组中删除元素,所以必须遍历编组的副本-->copy
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        # 检测子弹和外星人碰撞
        self._check_bullet_alien_collision()

    # 检测子弹和外星人碰撞
    def _check_bullet_alien_collision(self):
        # sprite.groupcollide将一个编组中的每个元素的rect同另一个编组中每个元素的rect进行比较，
        # 并返回一个字典，在这里 每个键都是一个子弹，关联的值是子弹射中的外星人
        # 两个实参True会让pygame删除碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            # 一颗子弹可能干掉多个敌人, 所以要遍历外星人
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            # 创建一副包含最新得分的新图像
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        # 创建一个外星人来计算一行可容纳多少个外星人
        alien = Alien(self)
        # 属性size是一个元组，包含rect对象的宽度和高度
        alien_width, alien_height = alien.rect.size
        # alien_width = alien.rect.width
        # 计算一行存放外星人的空间和数量
        available_space_x = self.settings.screen_width - (2 * alien_width)
        numbers_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # 创建外星人群
        for row_number in range(number_rows):
            # 创建第一行外星人
            for alien_number in range(numbers_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人并将其放置在首行
        alien = Alien(self)
        # alien_width = alien.rect.width
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        # 检测是否有外星人位于屏幕边缘
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船的碰撞
        # 遍历编组aliens 返回第一个与飞船碰撞的外星人
        # 如果没有发生碰撞 返回none，如果找到就返回这个外星人
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("ship hit!!!")
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        # 有外星人到达边缘时采取相应措施
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # 将外星人整体下移，并改变方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # 响应飞船被外星人碰撞
    def _ship_hit(self):
        if self.stats.ship_left > 0:
            # 删减剩下飞船数量 并更新记分牌
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            # 清空生下外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人，并将飞船移动到屏幕底端的中间
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    # 有外星人到达屏幕底端
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
