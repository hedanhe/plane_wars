import pygame
import random

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagess/enemy1_1.png")
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("imagess/enemy1_2.png").convert_alpha(), \
            pygame.image.load("imagess/enemy1_3.png").convert_alpha(), \
            pygame.image.load("imagess/enemy1_4.png").convert_alpha(), \
            pygame.image.load("imagess/enemy1_5.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = random.randint(1,3)
        self.active = True
        self.rect.left, self.rect.top = \
            random.randint(0, self.width - self.rect.width), \
            random.randint(-5* self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            random.randint(0, self.width - self.rect.width), \
            random.randint(-5 * self.height, -self.height)


class MidEnemy(pygame.sprite.Sprite):
    energy = 10
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("imagess/enemy2_1.png")
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("imagess/enemy2_2.png").convert_alpha(), \
            pygame.image.load("imagess/enemy2_3.png").convert_alpha(), \
            pygame.image.load("imagess/enemy2_4.png").convert_alpha(), \
            pygame.image.load("imagess/enemy2_5.png").convert_alpha(), \
            pygame.image.load("imagess/enemy2_6.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
            random.randint(0, self.width - self.rect.width), \
            random.randint(-5*self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = MidEnemy.energy

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
            random.randint(0, self.width - self.rect.width), \
            random.randint(-5 * self.height, -self.height)

class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("imagess/enemy3_1.png")
        self.image2 = pygame.image.load("imagess/enemy3_3.png")
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load("imagess/enemy3_3.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_4.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_5.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_6.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_7.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_8.png").convert_alpha(), \
            pygame.image.load("imagess/enemy3_9.png").convert_alpha()])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
            random.randint(0, self.width - self.rect.width), \
            random.randint(-15*self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = BigEnemy.energy


    def move(self):
        if self.rect.top < self.height :
            self.rect.top += self.speed
        else:
            self.reset()


    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = \
                    random.randint(0, self.width - self.rect.width), \
                    random.randint(-15 * self.height, -self.height)

