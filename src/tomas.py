import sys
import pygame as pg
import mygame as mg
from pygame.locals import *
from gameScene  import *



# 初期化と基本設定
pg.init()

screen = pg.display.set_mode((1000, 1000))
clock = pg.time.Clock()
framerate = 60

mg.init(screen, framerate)


# シーンの読み込み
menuScene = MenuScene()
playScene = PlayScene()


# 更新処理
while True:
    # フレームレート
    clock.tick(framerate)

    # 終了判定
    for e in pg.event.get():
        if e.type == QUIT: sys.exit()

    #menuScene.update()
    playScene.update()


    pg.display.update()
