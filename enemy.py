import pygame
import sys
from random import *
class smallenemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image=pygame.image.load("ui/shoot/enemy1.png").convert_alpha()
        self.destroy_image = []
        self.destroy_image.extend(\
            [pygame.image.load("ui/shoot/enemy1_down1.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy1_down2.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy1_down3.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy1_down4.png").convert_alpha()]\
            )
        self.active = True
        self.mask =pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.width,self.height =bg_size[0],bg_size[1]
        self.speed = 2
        
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-5*self.height,0)
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-5*self.height,0)
        
class midenemy(pygame.sprite.Sprite):
    energy = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("ui/shoot/enemy2.png").convert_alpha()
        self.destroy_image = []
        self.destroy_image.extend(\
            [pygame.image.load("ui/shoot/enemy2_down1.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy2_down2.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy2_down3.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy2_down4.png").convert_alpha()]\
            )
        self.active = True
        self.mask =pygame.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        self.width,self.height =bg_size[0],bg_size[1]
        self.speed = 1
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-10*self.height,-self.height)
        self.energy =midenemy.energy
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy =midenemy.energy
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-10*self.height,-self.height)
class bigenemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1=pygame.image.load("ui/shoot/enemy3_n1.png").convert_alpha()
        self.image2=pygame.image.load("ui/shoot/enemy3_n2.png").convert_alpha()
        self.destroy_image = []
        self.destroy_image.extend(\
            [pygame.image.load("ui/shoot/enemy3_down1.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy3_down2.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy3_down3.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy3_down4.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy3_down5.png").convert_alpha(),\
            pygame.image.load("ui/shoot/enemy3_down6.png").convert_alpha()]\
            )
        self.active = True
        self.mask =pygame.mask.from_surface(self.image1)
        self.rect=self.image1.get_rect()
        self.width,self.height =bg_size[0],bg_size[1]
        self.speed = 0.5
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-15*self.height,-5*self.height)
        self.energy =bigenemy.energy
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy =bigenemy.energy
        self.rect.left,self.rect.top =\
                                     randint(0,self.width -self.rect.width),\
                                     randint(-15*self.height,-5*self.height)
