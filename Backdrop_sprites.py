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

class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, WIDTH, HEIGHT, color, parralax_speed, screen_width):
        super().__init__()
        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parralex_speed = parralax_speed
        self.screen_width = screen_width
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parralex_speed

        if self.rect.right < 0:
            self.rect.left += self.screen_width *2
    def update(self):
        pass
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, parallax_speed, color, screen_width):
        super().__init__()
        self.image = pygame.Surface((140, 60), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (35, 35), 25)
        pygame.draw.circle(self.image, color, (70, 25), 30)
        pygame.draw.circle(self.image, color, (105, 35), 25)
        pygame.draw.rect(self.image, color, (30, 30, 85, 25))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parallax_speed = parallax_speed
        self.screen_width = screen_width
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parallax_speed
        if self.rect.right < 0:
            self.rect.left += self.screen_width *2 +random.randint(100, 300)
            self.rect.y = random.randint(50, 180)
    def update(self):
        pass
class Hill(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        parallax_speed,
        green_color,
        dark_green_color,
        screen_width,
        ):
        super().__init__()
        self.image = pygame.Surface((300, 180), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image,
            dark_green_color,
            [(0, 180), (150, 30), (300, 180)]
        )
        pygame.draw.polygon(
            self.image,
            green_color,
            [(40, 180), (150, 60), (260, 180)]
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.parallax_speed = parallax_speed
        self.screen_width = screen_width
    def move_with_camera(self, camera_dx):
        self.rect.x -= camera_dx * self.parallax_speed + 2
        if self.rect.right < 0:
            self.rect.left += self.screen_width * 2

    def update(self):
        pass

background_sprites = pygame.sprite.Group()
world_sprites = pygame.sprite.Group()