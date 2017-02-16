import pygame
import sys
from pygame.locals import *

pygame.init()

class MyPlane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        #加载飞机图片
        self.image1=pygame.image.load("ui/shoot/hero1.png").convert_alpha()
        self.image2=pygame.image.load("ui/shoot/hero2.png").convert_alpha()
        #加载飞机摧毁图片
        self.destroy_image = []
        self.destroy_image.extend(\
            [pygame.image.load("ui/shoot/hero_blowup_n1.png").convert_alpha(),\
            pygame.image.load("ui/shoot/hero_blowup_n2.png").convert_alpha(),\
            pygame.image.load("ui/shoot/hero_blowup_n3.png").convert_alpha(),\
            pygame.image.load("ui/shoot/hero_blowup_n4.png").convert_alpha()]\
            )
        self.active = True
        self.mask =pygame.mask.from_surface(self.image1)
        self.rect =self.image1.get_rect()
        (self.width ,self.height) =(bg_size[0],bg_size[1])
        (self.rect.left,self.rect.top)=((self.width - self.rect.width) // 2 , \
                                        self.height- self.rect.height-60)
        self.speed = 5
        self.invincible =False
    def moveup(self):
        if self.rect.top>0:
            self.rect.top -= self.speed
        else:
            self.rect.top =0
    def movedown(self):
        if self.rect.bottom <self.height-60:
            self.rect.top += self.speed
        else:
            self.rect.bottom =self.height-60
    def moveleft(self):
        if self.rect.left >0:
            self.rect.left -=self.speed
        else:
            self.rect.left=0
    def moveright(self):
        if self.rect.right <self.width:
            self.rect.left += self.speed
        else:
            self.rect.right =self.width
    def reset(self):
        self.active = True
        self.invincible =True
        (self.rect.left,self.rect.top)=((self.width - self.rect.width) // 2 , \
                                        self.height- self.rect.height-60)
        
        
    
