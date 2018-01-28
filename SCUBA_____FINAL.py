
import pygame, sys
from pygame.locals import *
import random
import time

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('SCUBA')

FPS = 30
fpsClock = pygame.time.Clock()


BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (119,136,153)
RED = (255,0,0)
PINK = (255,0,255)
DARKRED = (139,0,0)
GREEN = (0,255,0)
LIME = (0,255,0)
OLIVE = (85,107,47)
BLUE = (0,0,255)
DARKBLUE = (0,0,139)
AQUA = (0,255,255)
YELLOW = (255,255,0)
GOLD = (218,165,32)


class Swimmer(pygame.sprite.Sprite):
    SPEED = 12

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.imageSwim = pygame.image.load("scuba_diver.png") #http://openclipart.org/image/2400px/svg_to_png/29695/diver.png
        self.rect = self.imageSwim.get_rect()
        self.rect = Rect(self.rect.left+20, self.rect.top+30, self.rect.width-20, self.rect.height-20)
        self.rect.center = pos
        self.alive = True
 
    def draw(self, screen):
        screen.blit(self.imageSwim,self.rect)

    def handle_keystate(self, keys, screen):
        if keys[K_UP] and self.rect.top > 0:
            self.rect.top -= self.SPEED
        if keys[K_DOWN] and self.rect.bottom < screen.get_height():
            self.rect.top += self.SPEED
        if keys[K_RIGHT] and self.rect.right < screen.get_width():
            self.rect.right += self.SPEED
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.SPEED

class Shark(pygame.sprite.Sprite):
    SPEED = 8

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.imageShark = pygame.image.load("cartoon_shark.png") #http://www.clipartbest.com/cliparts/7ca/9br/7ca9brncA.jpeg
        self.rect2 = self.imageShark.get_rect()
        self.rect2 = Rect(self.rect2.left+75, self.rect2.top+40, self.rect2.width-40, self.rect2.height-30)
        self.rect2.center = pos
        self.onscreen = False
        self.visible = True

    def draw(self, screen):
        screen.blit(self.imageShark, self.rect2)

    def move(self, screen):
        self.rect2.left -= self.SPEED
        self.rect2.top += random.randint(-1,1)

        
            
            

class Powerup(pygame.sprite.Sprite):
    SPEED = 4
    counter = 0

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.imagePowerup = pygame.image.load("powerup1.png") #http://www.k6-geometric-shapes.com/image-files/circle-concentric.jpg
        self.rect3 = self.imagePowerup.get_rect()
        self.rect3 = Rect(self.rect3.left-5, self.rect3.top-5, self.rect3.width+5, self.rect3.height+5)
        self.rect3.center = pos
        self.onscreen = False
        self.visible = True
        
    def draw(self, screen):
        screen.blit(self.imagePowerup, self.rect3)

    def move(self, screen):
        self.rect3.left -= self.SPEED
        

class GameMain():
    done = False

    def __init__(self, width=800, height=400):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Don't Get Eaten")
        self.swimmer = Swimmer(pos=(width/6, height/2))
        self.shark = Shark(pos=(width+400, random.randint(0,height)))
        self.powerup = Powerup(pos=(width+25, random.randint(0,height))) 
        self.clock = pygame.time.Clock()
        self.shark_list = [self.shark]
        self.powerup_list = [self.powerup]
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        self.counter = 0
        self.gameover = False
        
        
    def main_loop(self):
        while not self.done:
            self.handle_events()
            self.swimmer.update()
            for shark in self.shark_list:
                shark.update()
            self.powerup.update()
            self.screen.fill(AQUA)
            self.draw()
            self.move()
            pygame.display.flip()
            self.clock.tick(60)
            for shark in self.shark_list:
                if shark.rect2.right < self.screen.get_width()-50 and shark.onscreen == False:
                    self.shark_list.append(Shark(pos=(self.screen.get_width()+225, random.randint(20,380))))
                    shark.onscreen = True
                if self.swimmer.rect.colliderect(shark.rect2):
                    self.swimmer.alive = False
                    self.gameover = True
            for powerup in self.powerup_list:
                if powerup.rect3.right < self.screen.get_width() - 700 and powerup.onscreen == False:
                    self.powerup_list.append(Powerup(pos=(self.screen.get_width()+25, random.randint(10,390))))
                    powerup.onscreen = True
                if self.swimmer.rect.colliderect(powerup.rect3) and powerup.visible:
                    powerup.visible = False
        if self.done:
            self.draw()
            self.handle_events()
            pygame.quit()
            sys.exit()
            
        

    def draw(self):
        for shark in self.shark_list:
            shark.draw(self.screen)
            if shark.rect2.right < self.screen.get_width() - 800 and not self.gameover and shark.visible == True:
                self.counter += 1
                shark.visible = False
        if self.swimmer.alive:
            self.swimmer.draw(self.screen)
        for powerup in self.powerup_list:
            if powerup.visible:
                powerup.draw(self.screen)
            if powerup.rect3.right < self.screen.get_width() - 800 and powerup.visible:
                self.gameover = True
        self.counter_text = self.fontObj.render(str(self.counter), True, BLACK)
        self.screen.blit(self.counter_text, (400,10))
        if self.gameover:
            self.screen.fill(AQUA)
            self.done1 = self.fontObj.render("Game Over", 1, BLACK)
            self.done2 = self.fontObj.render("Score: %d" % (self.counter), 1, BLACK)
            self.done3 = self.fontObj.render("Press [SPACE] to Play Again", 1, BLACK)
            self.screen.blit(self.done1, (325, 30))
            self.screen.blit(self.done2, (340, 100))
            self.screen.blit(self.done3, (200, 200))
            
            

    def move(self):
        for shark in self.shark_list:
            shark.move(self)
        for powerup in self.powerup_list:
            powerup.move(self)

    def handle_events(self):
        events = pygame.event.get()

        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT:
                self.done = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.done = True
                if self.gameover:
                    if event.key == K_SPACE:
                        self.__init__()
        self.swimmer.handle_keystate(keys, self.screen)
        

if __name__ == "__main__":
    game = GameMain()
    game.main_loop()

    
