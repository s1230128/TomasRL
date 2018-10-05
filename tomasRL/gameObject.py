import pygame as pg
import random
from math import sqrt, sin, cos, radians


# 初期化
def setup(screen):
    GameObject.screen = screen
    GameObject.screen_rect = screen.get_rect()


# GameObject
# オブジェクトのベースとなるクラス
class GameObject(pg.sprite.Sprite):
    containers = None
    imgPath = '../data/tomas.png'
    screen = None
    framerate = 60

    def __init__(self, pos, scale=None):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.image.load(self.imgPath).convert_alpha()
        if scale != None: self.image = pg.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()
        self.rect.center = pos


# Block
class Block(GameObject):
    imgPath = '../data/block.png'

    def __init__(self, pos, scale=None):
        GameObject.__init__(self, pos, scale)


# Paddle
class Paddle(GameObject):
    imgPath = '../data/tomas-paddle2.png'

    def __init__(self, pos, scale=None, speed=10):
        GameObject.__init__(self, pos, scale)

        self.speed = speed


    def step(self, act):
        # 左右に移動
        if act == 1: self.rect.centerx -= self.speed
        if act == 2: self.rect.centerx += self.speed

        # 画面端の判定
        if self.rect.left  < self.screen_rect.left : self.rect.left  = self.screen_rect.left
        if self.rect.right > self.screen_rect.right: self.rect.right = self.screen_rect.right


# Ball
class Ball(GameObject):
    imgPath = '../data/ball2.png'

    # pos : 画像の中心を表す座標
    def __init__(self, pos, scale=None, speed=10):
        GameObject.__init__(self, pos, scale)
        self.speed = speed

        #angle = radians(random.randint(45, 135))
        angle = 45
        self.vx = self.speed * cos(angle)
        self.vy = self.speed * sin(angle)

        self.done = False

    #
    def step(self):
        self.reward = 0

        # ボールの移動
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        rect = self.rect #self.rect は書き換えるため一旦コピーしてから比較する

        # スクリーン端の判定
        if rect.left   < self.screen_rect.left  : self.rect.left  = self.screen_rect.left ;\
                                                  self.vx = -self.vx
        if rect.right  > self.screen_rect.right : self.rect.right = self.screen_rect.right;\
                                                  self.vx = -self.vx
        if rect.top    < self.screen_rect.top   : self.rect.top   = self.screen_rect.top  ;\
                                                  self.vy = -self.vy
        if rect.bottom > self.screen_rect.bottom: self.done = True

        # 障害物との衝突判定
        for c in self.colliders:
            if self.rect.colliderect(c):
                '''
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
                '''
                ## パドル型との反射
                if type(c) is Paddle and self.vy > 0:
                    (x1, f1) = (c.rect.left - self.rect.width, 135)
                    (x2, f2) = (c.rect.right, 45)
                    x = self.rect.centerx
                    f = (float(f2-f1)/(x2-x1)) * (x - x1) + f1  # 線形補間
                    angle = radians(f)                          # 反射角度
                    self.vx =  self.speed * cos(angle)
                    self.vy = -self.speed * sin(angle)

        return self.done
