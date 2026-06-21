import pygame
import random

score = 0
timer = 0
WIDTH = 800
HEIGHT = 600
FPS = 60
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("mygame")
clock = pygame.time.Clock()
camera_border_x = WIDTH//3
spawn_distance = 300
world_offset = 0
next_ground_x = 0
coin_images_original = []
for i in range(17, 25):
    image = pygame.image.load(f"Tiles/{i}.png").convert_alpha()
    coin_images_original.append(image)

font = pygame.font.SysFont('arial', 36)

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
dark_green = (6,64,43)
ground_y = HEIGHT -50
TILE_SIZE = 41
gravity = 0.3

ground_img = pygame.image.load('Tiles/ground.png').convert_alpha()
platform_img = pygame.image.load('Tiles/platform.png').convert_alpha()
player_img = pygame.image.load('Tiles/player.png').convert_alpha()
ground1_img = pygame.image.load('Tiles/ground1,2,3layers.png').convert_alpha()
realcoin_img = pygame.image.load('Tiles/realcoin.png').convert_alpha()
startrun_img = pygame.image.load('Tiles/startrun.png').convert_alpha()
startrun1_img = pygame.image.load('Tiles/startrun1.png').convert_alpha()
run_img = pygame.image.load('Tiles/run.png').convert_alpha()
run1_img = pygame.image.load('Tiles/run1.png').convert_alpha()
endrun_img = pygame.image.load('Tiles/endrun.png').convert_alpha()
jump_img = pygame.image.load('Tiles/jump.png').convert_alpha()
jump_img1 = pygame.image.load('Tiles/jump1.png').convert_alpha()
jump_img2 = pygame.image.load('Tiles/jump2.png').convert_alpha()

ground_img = pygame.transform.scale(ground_img, (TILE_SIZE, TILE_SIZE))
platform_img = pygame.transform.scale(platform_img, (TILE_SIZE, TILE_SIZE/2))
player_img = pygame.transform.scale(player_img, (40, 50))
ground1_img = pygame.transform.scale(ground1_img, (TILE_SIZE, TILE_SIZE))
realcoin_img = pygame.transform.scale(realcoin_img, (TILE_SIZE, TILE_SIZE))
startrun_img = pygame.transform.scale(startrun_img, (40, 50))
startrun1_img = pygame.transform.scale(startrun1_img, (40, 50))
run_img = pygame.transform.scale(run_img, (40, 50))
run1_img = pygame.transform.scale(run1_img, (40, 50))
endrun_img = pygame.transform.scale(endrun_img, (40, 50))
jump_img = pygame.transform.scale(jump_img, (40, 40))
jump_img1 = pygame.transform.scale(jump_img1, (40, 50))
jump_img2 = pygame.transform.scale(jump_img2, (40, 50))

def flip_image(image):
    return pygame.transform.flip(image, True, False)
player_idle_right = player_img
player_jump_right = [
    jump_img,
    jump_img1,
    jump_img2
]
player_walk_right = [
    startrun_img,
    startrun1_img,
    run_img,
    run1_img,
    endrun_img,
]
player_idle_left = flip_image(player_idle_right)
player_jump_left = []
for image in player_jump_right:
    player_jump_left.append(flip_image(image))
player_walk_left = []
for image in player_walk_right:
    player_walk_left.append(flip_image(image))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.on_ground = True

        self.idle_right = player_idle_right
        self.idle_left = player_idle_left

        self.walk_right = player_walk_right
        self.walk_left = player_walk_left

        self.jump_right = player_jump_right
        self.jump_left = player_jump_left

        self.animation_index = 0
        self.animation_speed = 0.15

        self.direction = "right"

        self.image = self.idle_right
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.vel_x = 0
        self.speed_x = 0
        self.speed_y = 0
    def animate (self):
        old_midbottom = self.rect.midbottom

        if self.direction == "right":
            idle_image = self.idle_right
            walk_images = self.walk_right
            jump = player_jump_right
        else:
            idle_image = self.idle_left
            walk_images = self.walk_left
            jump = player_jump_left
        if not self.on_ground:
            if self.speed_y > -2 and self.speed_y < 2:
                jump_image = jump[1]
            elif self.speed_y < -2:
                jump_image = jump[0]
            elif self.speed_y > 2:
                jump_image = jump[2]
            current_image = jump_image
        elif abs(self.vel_x) > 0.2:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(walk_images):
                self.animation_index = 0
            current_image = walk_images[int(self.animation_index)]
        else:
            self.animation_index = 0
            current_image = idle_image
        self.image = current_image
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom
    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.x += self.vel_x
        if self.rect.x <= 0:
            self.rect.x = 0
            self.vel_x = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.vel_x -= 0.5
            if self.vel_x <= -5:
                self.vel_x = -5
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            self.vel_x += 0.5
            if self.vel_x >= 5:
                self.vel_x = 5
            self.direction = "right"
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
        self.on_ground = False
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


        self.animate()
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def update(self):
        pass
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, images):
        super().__init__()

        self.radius = radius
        self.images = []
        for image in images:
            scaled_image = pygame.transform.scale(
                image,
                (radius * 2, radius * 2)
            )
            self.images.append(scaled_image)
        self.current_frame = 0
        self.frame_timer = 0
        self.frames_per_image = 10
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        if radius == 24:
            self.price = 3
        elif radius == 12:
            self.price = 2
        elif radius == 6:
            self.price = 1

    def animate(self):
        old_center = self.rect.center

        self.frame_timer += 1
        if self.frame_timer >= self.frames_per_image:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.current_frame = 0
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.animate()

        if self.rect.right < -200:
            self.kill()

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, WIDTH, HEIGHT, color, parralax_speed):
        super().__init__()
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parralex.speed = parralax_speed
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parralax_speed

        if self.rect.right < 0:
            self.rect.left += WIDTH *2
    def update(self):
        pass
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, parallax_speed):
        super().__init__()
        self.image = pygame.Surface((140, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, white, (35, 35), 25)
        pygame.draw.circle(self.image, white, (70, 25), 30)
        pygame.draw.circle(self.image, white, (105, 35), 25)
        pygame.draw.rect(self.image, white, (30, 30, 85, 25))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parallax_speed = parallax_speed
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parallax_speed
        if self.rect.right < 0:
            self.rect.left += WIDTH *2 +random.randit(100, 300)
            self.rect.y = random.randit(50, 180)
    def update(self):
        pass
class hill(pygame.sprite.Sprite):
    def __init__(self, x, y, parallax_speed):
        super().__init__()
        self.image = pygame.Surface((300, 180), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            dark_green,
            [(0, 180), (150, 30), (300, 180)]
        )
        pygame.draw.polygon(
            self.image,
            green,
            [(40, 180), (150, 60), (260, 180)]
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parallax_speed = parallax_speed
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parallax_speed + 2
        if self.rect.right < 0:
            self.rect.left += WIDTH * 2 + random.randit(100, 300)
            self.rect.y = random.randit(50, 180)
    def update(self):
        pass







coin1 = Coin(250, 370, 6, coin_images_original)
coin2 = Coin(560, 270, 12, coin_images_original)
coin3 = Coin(150, 220, 12, coin_images_original)
coin4 = Coin(700, 300, 24, coin_images_original)
coin5 = Coin(150, 370, 6, coin_images_original)
coin6 = Coin(730, 370, 6, coin_images_original)
coin7 = Coin(350, 370, 24, coin_images_original)

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
    ground1 = Platform(x, HEIGHT - TILE_SIZE, ground1_img)

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

    (250, 100, platform_img),
    (291, 100, platform_img),
    (332, 100, platform_img),

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

