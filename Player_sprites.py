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
sky_blue = (135, 206, 235)
ground_y = HEIGHT -50
TILE_SIZE = 41
gravity = 0.3


ground_img = pygame.image.load('Tiles/ground.png').convert_alpha()
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
    def __init__(
            self,
            idle_right,
            idle_left,
            walk_right,
            walk_left,
            jump_right,
            jump_left,

            ):
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

    def update(self, platforms, WIDTH, gravity):
        keys = pygame.key.get_pressed()

        # ---------------- JUMP ----------------

        if keys[pygame.K_SPACE] and self.on_ground:
            self.speed_y = -10
            self.on_ground = False

        # ---------------- X SPEED ----------------

        if keys[pygame.K_LEFT]:
            self.vel_x -= 0.5
            self.direction = "left"

            if self.vel_x <= -5:
                self.vel_x = -5

        elif keys[pygame.K_RIGHT]:
            self.vel_x += 0.5
            self.direction = "right"

            if self.vel_x >= 5:
                self.vel_x = 5

        else:
            self.vel_x *= 0.97

            if abs(self.vel_x) < 0.1:
                self.vel_x = 0

        # ---------------- X MOVEMENT ----------------

        old_rect_x = self.rect.copy()

        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x = 0

        hits_x = pygame.sprite.spritecollide(self, platforms, False)

        for platform in hits_x:
            if self.vel_x > 0 and old_rect_x.right <= platform.rect.left:
                self.rect.right = platform.rect.left
                self.vel_x = 0

            elif self.vel_x < 0 and old_rect_x.left >= platform.rect.right:
                self.rect.left = platform.rect.right
                self.vel_x = 0

        # ---------------- Y MOVEMENT ----------------

        old_rect_y = self.rect.copy()

        self.speed_y += gravity

        if self.speed_y > 10:
            self.speed_y = 10

        self.rect.y += self.speed_y

        self.on_ground = False

        hits_y = pygame.sprite.spritecollide(self, platforms, False)

        for platform in hits_y:
            if self.speed_y > 0 and old_rect_y.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.speed_y = 0
                self.on_ground = True

            elif self.speed_y < 0 and old_rect_y.top >= platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.speed_y = 0

        # ---------------- ANIMATION ----------------

        self.animate()
class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        bottom_y,
        platforms,
        speed = 1.5,
        gravity= 0.3
    ):
        super().__init__()
        self.platforms = platforms
        self.speed = abs(speed)
        self.gravity = gravity
        self.speed_y = 0
        self.images = [
            self.create_image(left_foot_up= False),
            self.create_image(left_foot_up= True),
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frames_per_image = 12
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, bottom_y)
    @staticmethod
    def create_image(left_foot_up = False):
        image = pygame.Surface ((40, 34), pygame.SRCALPHA)
        pygame.draw.ellipse(image, (180,70,35), [3, 3, 34, 27])
        pygame.draw.ellipse(image, (225, 105, 45), [7, 1, 26, 18])
        pygame.draw.circle(image, (255, 255, 255), (15, 13), 4)
        pygame.draw.circle(image, (255, 255, 255), (25, 13), 4)
        pygame.draw.circle(image, (20, 20, 20), (14, 14), 2)
        pygame.draw.circle(image, (20, 20, 20), (24, 14), 2)
        if left_foot_up:
            pygame.draw.ellipse(image, (70, 35, 20), [3, 27, 15, 6])
            pygame.draw.ellipse(image, (70, 35, 20), [23, 25, 15, 8])
        else:
            pygame.draw.ellipse(image, (70, 35, 20), [3, 25, 15, 8])
            pygame.draw.ellipse(image, (70, 35, 20), [23, 27, 15, 6])
        return image
    def animate(self):
        old_midbottom = self.rect.midbottom
        self.frame_timer += 1
        if self.frame_timer >= self.frames_per_image:
            self.frame_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.current_frame = 0
            self.image = self.images[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = old_midbottom
    def update(self):
        self.rect.x -= self.speed
        old_rect_y = self.rect.copy()
        self.speed_y += self.gravity
        if self.speed_y > 10:
            self.speed_y = 10
        self.rect.y += self.speed_y
        hits_y = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in hits_y:
            if self.speed_y > 0 and old_rect_y.bottom <= platform.rect.top:
                self.rect.bottom = platform.rect.top
                self.speed_y = 0
                break
        self.animate()
        if self.rect.right < -200 or self.rect.top > 800:
            self.kill()
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

player = Player(
    player_idle_right,
    player_idle_left,
    player_walk_right,
    player_walk_left,
    player_jump_right,
    player_jump_left,
)

platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
