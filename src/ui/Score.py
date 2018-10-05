# スコアのクラス
class Score():
    def __init__(self, pos, font=None):
        self.score = 0
        self.x, self.y = pos
        self.font = pygame.font.SysFont(font, 20)
        
    def draw(self, screen):
        img = self.font.render("SCORE:"+str(self.score), True, (255,255,250))
        screen.blit(img, (self.x, self.y))
        
    def add_score(self, x):
        self.score += x