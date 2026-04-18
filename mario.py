import platform

import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 60
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128,0,128)
orange = (255,165,0)
brown = (165,42,42)
lemonsomething = (255,250,205)
yellow = (255,255,0)
cyan = (0,255,255)
ground_y = HEIGHT -50

gravity = 0.5

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.vel_x = 0
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        keys = pygame.key.get_pressed()
        if self.rect.bottom <= ground_y:
            #self.speed_y += gravity
            self.rect.y += self.speed_y
        else:
            self.speed_y = 0
            self.rect.bottom = ground_y

        self.rect.x += self.vel_x
        if self.rect.x <= 0:
            self.rect.x = 0
            self.vel_x = 5
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.vel_x = -5

        if keys[pygame.K_LEFT]:
            self.vel_x -= 0.5
            if self.vel_x <= -5:
                self.vel_x = -5
        if keys[pygame.K_RIGHT]:
            self.vel_x += 0.5
            if self.vel_x >= 5:
                self.vel_x = 5


        else:
            self.speed_y += gravity
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for platform in hits:
                if self.speed_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.speed_y = 0
                    self.on_ground = True

                elif self.speed_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.speed_y = 0
            if keys[pygame.K_SPACE] and self.on_ground == True:
                self.speed_y = - 10

        self.on_ground = False
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        pass
platform1 = Platform(200, 370, 150, 20)
platform2 = Platform(150, 100, 150, 20)
ground = Platform(0, 550, 800, 50)
player = Player()
platforms = pygame.sprite.Group()
platforms.add(platform1)
platforms.add(ground)
platforms.add(platform2)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)
all_sprites.add(ground)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    screen.fill(white)
    all_sprites.draw(screen)
    pygame.display.flip()
