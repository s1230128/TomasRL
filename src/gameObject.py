import pygame as pg
import mygame as mg
from pygame.locals import *
from math import sqrt, sin, cos, radians



# Block
class Block(mg.GameObject):
    imgPath = '../data/block.png'

    # pos : 画像の中心を表す座標
    def __init__(self, pos):
        mg.GameObject.__init__(self, pos)



# Paddle
class Paddle(mg.GameObject):
    imgPath = '../data/tomas-paddle2.png'

    # pos   : 画像の中心を表す座標
    # speed : 移動速度
    # fric  : 摩擦力
    def __init__(self, pos, scale=None, speed=500, fric=1000):
        mg.GameObject.__init__(self, pos, scale)

        self.direction = 0
        self.speed = speed
        self.fric = fric
        self.image = pg.transform.scale(self.image, (self.rect.width * 3, self.rect.height * 3))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    #
    def update(self):
        # 矢印キーで左右に移動
        self.direction = 0
        if pg.key.get_pressed()[K_LEFT ]: self.direction -= 1
        if pg.key.get_pressed()[K_RIGHT]: self.direction += 1

        self.rect.centerx += (self.direction * self.speed) / self.framerate

        # 画面端の判定
        if self.rect.left  < self.screen_rect.left : self.rect.left  = self.screen_rect.left
        if self.rect.right > self.screen_rect.right: self.rect.right = self.screen_rect.right



# Ball
class Ball(mg.GameObject):
    imgPath = '../data/ball2.png'
    colliders = pg.sprite.Group()

    # pos : 画像の中心を表す座標
    # v   : ボールの初速
    def __init__(self, pos, speed):
        mg.GameObject.__init__(self, pos)

        self.speed = speed
        self.vx = 0
        self.vy = -speed
        self.init_pos   = pos

    #
    def update(self):
        # ボールの移動
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        # オブジェクトとの衝突判定
        rect = self.rect #self.rect は書き換えるため一旦コピーしてから比較する

        # スクリーン端の判定
        if rect.left   < self.screen_rect.left  : self.rect.left  = self.screen_rect.left ;\
                                                  self.vx = -self.vx + 10
        if rect.right  > self.screen_rect.right : self.rect.right = self.screen_rect.right;\
                                                  self.vx = -self.vx - 10
        if rect.top    < self.screen_rect.top   : self.rect.top   = self.screen_rect.top  ;\
                                                  self.vy = -self.vx + 10
        if rect.bottom > self.screen_rect.bottom: self.rect.center = self.init_pos;\
                                                  self.dx = 0;\
                                                  self.dy = -self.speed


        # 障害物との衝突判定
        for c in self.colliders:
            if self.rect.colliderect(c):
                ## ブロック型との反射
                if type(c) is Block:
                    if rect.left   < c.rect.left  : self.rect.right  = c.rect.left  ;\
                                                    self.vx = -self.vx
                    if rect.right  > c.rect.right : self.rect.left   = c.rect.right ;\
                                                    self.vx = -self.vx
                    if rect.top    < c.rect.top   : self.rect.bottom = c.rect.top   ;\
                                                    self.vy = -self.vy
                    if rect.bottom > c.rect.bottom: self.rect.top    = c.rect.bottom;\
                                                    self.vy = -self.vy
                    c.kill()

                ## パドル型との反射
                if type(c) is Paddle and self.vy > 0:
                    (x1, f1) = (c.rect.left - self.rect.width, 135)
                    (x2, f2) = (c.rect.right, 45)
                    x = self.rect.centerx
                    f = (float(f2-f1)/(x2-x1)) * (x - x1) + f1  # 線形補間
                    angle = radians(f)                          # 反射角度
                    self.vx =  self.speed * cos(angle)
                    self.vy = -self.speed * sin(angle)



'''
# Enemy
class Enemy(mg.GameObject):
    imgPath = '../data/tomas.png'

    # pos : 画像の中心を表す座標
    def __init__(self, pos, scale=None):
        mg.GameObject.__init__(self, pos, scale)

    def update():
        self.image = pg.transform.rotate(self.image, angle=2)
'''
