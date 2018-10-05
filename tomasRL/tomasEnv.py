import sys
import math
import numpy  as np
import pygame as pg
from pygame.locals import *

import gameObject


#
class TomasEnv:
    #
    def __init__(self):
        # 初期化と基本設定
        pg.init()
        self.screen = pg.display.set_mode((400, 700))

        gameObject.setup(self.screen)

        # グループ設定
        self.render_group   = pg.sprite.RenderUpdates()
        self.collider_group = pg.sprite.Group()

        gameObject.Paddle.containers = self.render_group, self.collider_group
        gameObject.Ball.containers   = self.render_group
        gameObject.Ball.colliders    = self.collider_group

        self.reset()

    #
    def reset(self):
        # オブジェクト全削除
        self.render_group.empty()
        self.collider_group.empty()

        # オブジェクトの生成と配置
        self.ball   = gameObject.Ball((200, 100), speed=5)
        self.paddle = gameObject.Paddle((200, 600), scale=(152, 44), speed=5)

        return self.__obs()

    #
    def step(self, action):
        self.paddle.step(action)
        self.ball.step()

        self.obs = self.__obs()
        self.b_x, self.b_y = self.ball.rect.center
        self.p_x, self.p_y = self.paddle.rect.center

        self.reward = 900 - math.sqrt((self.b_x - self.p_x)**2 + (self.b_y - self.p_y)**2)
        self.done = self.ball.step()
        self.info = None

        return self.obs, self.reward, self.done, self.info

    #
    def __obs(self):
        self.p_x , self.p_y  = self.paddle.rect.center
        self.b_x , self.b_y  = self.ball.rect.center
        self.b_vx, self.b_vy = self.ball.vx, self.ball.vy

        return np.array([self.p_x, self.p_y, self.b_x, self.b_y, self.b_vx, self.b_vy], dtype=np.float32)

    #
    def render(self):
        self.screen.fill((10, 10, 10))
        self.render_group.update()
        self.render_group.draw(self.screen)

        pg.display.update()

    #
    def random_act(self):
        return np.random.choice([0, 1, 2])



# main
if __name__ == '__main__':
    env = TomasEnv()

    clock = pg.time.Clock()
    framerate = 60
    done = False

    while not done:
        # フレームレート
        clock.tick(framerate)

        # 終了判定
        for e in pg.event.get():
            if e.type == QUIT: sys.exit()

        act = 0
        if pg.key.get_pressed()[K_LEFT ]: act = 1
        if pg.key.get_pressed()[K_RIGHT]: act = 2

        obs, reward, done, info = env.step(act)
        env.render()
