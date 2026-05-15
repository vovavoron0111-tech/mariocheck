import platform

import pygame
import random
score = 0
timer = 0
WIDTH = 800
HEIGHT = 600
FPS = 60
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont('arial', 36)
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
TILE_SIZE = 41
gravity = 0.3

ground_img = pygame.image.load('Tiles/ground.png').convert_alpha()
platform_img = pygame.image.load('Tiles/platform.png').convert_alpha()
player_img = pygame.image.load('Tiles/player.png').convert_alpha()
ground1_img = pygame.image.load('Tiles/ground1,2,3layers.png').convert_alpha()

ground_img = pygame.transform.scale(ground_img, (TILE_SIZE, TILE_SIZE))
platform_img = pygame.transform.scale(platform_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (40, 50))
ground1_img = pygame.transform.scale(ground1_img, (TILE_SIZE, TILE_SIZE))


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
        elif keys[pygame.K_RIGHT]:
            self.vel_x += 0.5
            if self.vel_x >= 5:
                self.vel_x = 5
        else:
            self.vel_x *= 0.97
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.vel_x > 0:
                self.rect.right = platform.rect.left
                self.vel_x = 0

            elif self.vel_x < 0:
                self.rect.left = platform.rect.right
                self.vel_x = 0

        #x-movement end
        #y-movement beginning

        self.speed_y += gravity
        self.rect.y += self.speed_y

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
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        pass
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, yellow, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        if radius == 24:
            self.price = 3
        elif radius == 12:
            self.price = 2
        elif radius == 6:
            self.price = 1

    def update(self):
        pass



coin1 = Coin(250, 370, 6)
coin2 = Coin(560, 270, 12)
coin3 = Coin(150, 220, 12)
coin4 = Coin(700, 500, 24)
coin5 = Coin(150, 370, 6)
coin6 = Coin(730, 370, 6)
coin7 = Coin(350, 370, 24)

player = Player()

platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()



all_sprites.add(player)
all_sprites.add(platforms)

all_sprites.add(coin1, coin2, coin3, coin4, coin5, coin6, coin7)
coins.add(coin1, coin2, coin3, coin4, coin5, coin6, coin7)
for x in range(0, WIDTH, TILE_SIZE):
    ground = Platform(x, HEIGHT - 82 - TILE_SIZE, ground_img)

    all_sprites.add(ground)
    platforms.add(ground)

for x in range(0, WIDTH, TILE_SIZE):
    ground1 = Platform(x, HEIGHT - 41 - TILE_SIZE, ground1_img)

    all_sprites.add(ground1)
    platforms.add(ground1)

for x in range(0, WIDTH, TILE_SIZE):
    ground = Platform(x, HEIGHT - TILE_SIZE, ground1_img)

    all_sprites.add(ground1)
    platforms.add(ground1)

platform_positions = [
    (200, 450, platform_img),
    (242, 450, platform_img),
    (284, 450, platform_img),

    (400, 350, platform_img),
    (442, 350, platform_img),
    (484, 350, platform_img),


    (150, 250, platform_img),
    (192, 250, platform_img),

    (250, 150, platform_img),
    (291, 150, platform_img),
    (332, 150, platform_img),

]


for pos in platform_positions:
    platform = Platform(pos[0], pos[1], platform_img)
    all_sprites.add(platform)
    platforms.add(platform)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    for coin in  collected_coins:
        score += coin.price


    screen.fill(white)
    all_sprites.draw(screen)
    timer += 1
    score_text = font.render(f'Coins: {score}', True, black)
    time_text = font.render(f'Time: {timer}', True, black)
    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (500, 20))
    pygame.display.flip()

