from random import *
import pygame
import time
from constants import *
from objects.ball import BallObject
from objects.platform import PlatformObject
from objects.text import TextObject
from scenes.base import BaseScene
from fileuploader import FileUploader


class GameScene(BaseScene):
    collision_tolerance = 100
    standart_speed = randrange(2, 3)
    accelerate = 1.15
    max_collisions = 20

    def __init__(self, game):
        super().__init__(game)
        self.start_time = time.time()
        self.platform = PlatformObject(game, speed=GameScene.standart_speed)
        self.ball = [BallObject(game, speed=[GameScene.standart_speed, GameScene.standart_speed])]
        self.collision_count = 0
        self.score_text = TextObject(self.game, 0, 0, self.get_score_text(), ORANGE)
        self.score_text.move(10, 10)
        self.objects += self.ball
        self.objects.append(self.score_text)
        self.objects.append(self.platform)
        self.reset_balls_position()

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.set_scene(self.game.SCENE_MENU)
            elif event.key == pygame.K_a or event.key == pygame.K_d:
                self.platform.process_event(event)

    def update_score(self):
        self.score_text.update_text(self.get_score_text())
        self.score_text.move(10, 10)

    def get_score(self):
        return int(time.time() - self.start_time)

    def get_score_text(self):
        return f'Score: {self.get_score()} seconds'

    def get_random_position(self, radius):
        return randint(10, self.game.width - radius * 2 - 10), randint(10, self.game.height - radius * 2 - 300)

    def set_random_position(self, ball):
        pos = self.get_random_position(ball.radius)
        ball.move(*pos)

    def reset_balls_position(self):
        for ball in self.ball:
            ball.move(self.game.width, self.game.height)

    def set_random_unique_position(self):
        for index in range(len(self.ball)):
            other_rect = [self.ball[i].rect for i in range(len(self.ball)) if i != index]
            self.set_random_position(self.ball[index])
            while self.ball[index].rect.collidelist(other_rect) != -1:
                self.set_random_position(self.ball[index])

    def on_activate(self):
        self.start_time = time.time()
        self.reset_balls_position()
        self.set_random_unique_position()
        self.score_text.update_text(self.get_score_text())
        self.score_text.move(10, 10)

    def collide_platform_with_ball(self):
        if self.platform.rect.colliderect(self.ball[0].rect):
            if abs(self.ball[0].rect.bottom - self.platform.rect.top) < GameScene.collision_tolerance and \
                    self.ball[0].speed[1] > 0:
                self.ball[0].speed[1] *= -GameScene.accelerate
            elif abs(self.ball[0].rect.left - self.platform.rect.right) < GameScene.collision_tolerance and \
                    self.ball[0].speed[0] < 0:
                self.ball[0].speed[0] *= -GameScene.accelerate
            elif abs(self.ball[0].rect.right - self.platform.rect.left) < GameScene.collision_tolerance and\
                    self.ball[0].speed[0] > 0:
                self.ball[0].speed[0] *= -GameScene.accelerate
            self.collision_count += 1

    def check_game_over(self):
        if self.ball[0].rect.bottom >= self.game.height or self.collision_count == GameScene.max_collisions:
            self.game.fileul.set_score(self.get_score())
            self.game.fileul.write_file_data()
            if self.collision_count == GameScene.max_collisions:
                self.game.set_scene(self.game.SCENE_GAMEWIN)
            else:
                self.game.set_scene(self.game.SCENE_GAMEOVER)
            self.collision_count = 0
            self.start_time = 0

    def process_logic(self):
        super().process_logic()
        self.collide_platform_with_ball()
        self.update_score()
        self.check_game_over()
