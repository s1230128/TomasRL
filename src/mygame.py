import pygame as pg



def init(screen, framerate):
    GameObject.screen = screen
    GameObject.screen_rect = screen.get_rect()
    GameObject.framerate = framerate

    GameScene.screen = screen
    GameScene.screen_rect = screen.get_rect()
    GameScene.framerate = framerate



# GameObject
# オブジェクトのベースとなるクラス
class GameObject(pg.sprite.Sprite):
    imgPath = '../data/tomas.png'

    # pos : 画像の中心を表す座標
    def __init__(self, pos, scale=None):
        pg.sprite.Sprite.__init__(self, self.containers)

        self.image = pg.image.load(self.imgPath).convert_alpha()
        if scale != None: self.image = pg.transform.scale(self.image, scale)

        self.rect = self.image.get_rect()
        self.rect.center = pos





# GameScene
# シーンのベースとなるクラス
class GameScene:
    def init(self):
        pass

    def update(self):
        pass
