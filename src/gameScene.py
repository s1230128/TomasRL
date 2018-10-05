import pygame as pg
import mygame as mg
from gameObject import *



#
class PlayScene(mg.GameScene):
    def __init__(self):
        ## グループ設定
        self.render_group   = pg.sprite.RenderUpdates()
        self.collider_group = pg.sprite.Group()

        Block.containers  = self.render_group, self.collider_group
        Paddle.containers = self.render_group, self.collider_group
        Ball.containers   = self.render_group
        Ball.colliders    = self.collider_group
        #Enemy.containers  = self.render_group

        # オブジェクトの生成と配置
        self.blocks = []
        for i in range(1, 20):
            for j in range(1, 15):
                self.block = Block((25 * i, 15 * j))
                self.blocks.append(self.block)

        self.ball = Ball((250, 250), speed=20)

        self.paddle = Paddle((250, 600), speed=100, fric=0.5)
        #self.enemy = Enemy((700, 200))


    def update(self):
        self.screen.fill((10, 10, 10))
        self.render_group.update()
        self.render_group.draw(self.screen)


#
class MenuScene(mg.GameScene):
    def __init__(self):
        pass


    def update(self):
        self.screen.fill((50, 100, 50))
