import pygame
import random

class Bullet_supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagess/bullet_supply.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
            random.randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False

    def move(self):
        self.rect.top += self.speed

        if self.rect.top > self.height:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
            random.randint(0, self.width - self.rect.width), -100

class Bomb_supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagess/bomb_supply.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
            random.randint(0, self.width - self.rect.width), -100

        self.speed = 5
        self.active = False

    def move(self):
        self.rect.top += self.speed

        if self.rect.top > self.height:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
            random.randint(0, self.width - self.rect.width), -100