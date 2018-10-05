import sys
import numpy as np
import pygame as pg
from pygame.locals import *
import tomasEnv


#
if __name__ == '__main__':
    env = tomasEnv.TomasEnv()

    clock = pg.time.Clock()
    framerate = 60
    done = False

    while not done:
        # フレームレート
        clock.tick(framerate)

        # 終了判定
        for e in pg.event.get():
            if e.type == QUIT: sys.exit()

        '''
        act = 0
        if pg.key.get_pressed()[K_LEFT ]: act = 1
        if pg.key.get_pressed()[K_RIGHT]: act = 2
        '''
        act = env.random_act()

        obs, reward, done, info = env.step(act)
        env.render()
