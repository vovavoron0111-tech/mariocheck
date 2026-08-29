import pygame



HEIGHT = 600


TILE_SIZE = 41
platform_img = pygame.image.load('Tiles/platform.png').convert_alpha()
platform_img = pygame.transform.scale(platform_img, (TILE_SIZE, TILE_SIZE/2))
def get_platform_plan(platform_img):
    return [
    {
        "x_start": 200,
        "y_start": 450,
        "count": 3,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 400,
        "y_start": 350,
        "count": 3,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 150,
        "y_start": 250,
        "count": 2,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 250,
        "y_start": 100,
        "count": 3,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 850,
        "y_start": 430,
        "count": 4,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 1100,
        "y_start": 320,
        "count": 3,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 1400,
        "y_start": 230,
        "count": 5,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 1750,
        "y_start": 380,
        "count": 2,
        "images": [platform_img],
        "spawned": False,
     },
]
def get_coin_plan(coin_images_original):
    return [
    {
        "x_start": 250,
        "y_start": 370,
        "radius": 6,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 560,
        "y_start": 270,
        "radius": 12,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 150,
        "y_start": 220,
        "radius": 12,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 700,
        "y_start": 300,
        "radius": 24,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 900,
        "y_start": 380,
        "radius": 6,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 1150,
        "y_start": 280,
        "radius": 12,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 1450,
        "y_start": 190,
        "radius": 24,
        "images": coin_images_original,
        "spawned": False,
    },
    {
        "x_start": 1800,
        "y_start": 330,
        "radius": 12,
        "images": coin_images_original,
        "spawned": False,
    },
]
def get_enemy_plan():
    ground_top_y = HEIGHT - TILE_SIZE * 3
    return [
    {
        "x": 1720,
        "bottom_y": ground_top_y,
        "speed": 1.4,
        "spawned": False,
    },
    {
        "x": 950,
        "bottom_y": 430,
        "speed": 1.2,
        "spawned": False,
    },
    ]
