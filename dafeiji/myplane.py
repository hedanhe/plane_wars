import pygame
from pygame.locals import *

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("imagess/hero1_1.png").convert_alpha()
        self.image2 = pygame.image.load("imagess/hero2_1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load("imagess/hero1_2.png").convert_alpha(), \
            pygame.image.load("imagess/hero1_3.png").convert_alpha(), \
            pygame.image.load("imagess/hero1_4.png").convert_alpha(), \
            pygame.image.load("imagess/hero1_5.png").convert_alpha()])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left = (self.width - self.rect.width)//2
        self.rect.top = self.height - self.rect.height - 50
        self.speed = 10
        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)

    def movup(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def movdown(self):
        if self.rect.bottom < self.height:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height

    def movleft(self):
        if self.rect.left > -10:
            self.rect.left -= self.speed
        else:
            self.rect.left = -10

    def movright(self):
        if self.rect.right < self.width + 10:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width + 10

    def reset(self):
        self.active = True
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = self.height - self.rect.height - 50