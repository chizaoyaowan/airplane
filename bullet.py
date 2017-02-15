import pygame

class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("ui/shoot/bullet1.png").convert_alpha()
        self.rect =self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = 10
        self.active =True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):

        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active =False

    def reset(self,position):
        self.rect.left,self.rect.top =position
        self.active =True

class Bullet2(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("ui/shoot/bullet2.png").convert_alpha()
        self.rect =self.image.get_rect()
        self.rect.left,self.rect.top = position
        self.speed = 10
        self.active =True
        self.mask=pygame.mask.from_surface(self.image)

    def move(self):

        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active =False

    def reset(self,position):
        self.rect.left,self.rect.top =position
        self.active =True
