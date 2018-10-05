import pygame as pg
from pygame.locals import *
import sys


    
def detectQuit():
    for e in pg.event.get(): 
        if e.type == QUIT: sys.exit()


#
pg.init()
pg.display.set_caption('Pygame demo 2')

screen = pg.display.set_mode((560, 372))
    
x, y = 0, 0
        
bg = pg.image.load('bandai.jpg').convert_alpha()
bg = pg.transform.scale(bg, (560, 372))
rect_bg = bg.get_rect()   
        
bl = pg.image.load('tomas.png').convert_alpha()
bl = pg.transform.scale(bl, ( 99,  99))
rect_bl = bl.get_rect()  

print(type(bl))
print(type(rect_bl))

print(SCREEN.left)
print(SCREEN.right)


while True:
    detectQuit()
        
    x = x + 1
    y = y + 1
    rect_bl.center = (x, y)
        
    screen.fill(pg.Color(0, 0, 0))
    screen.blit(bg, rect_bg)
    screen.blit(bl, rect_bl) 
        
    pg.display.update()
    