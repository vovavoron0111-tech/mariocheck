import pygame



HEIGHT = 600


TILE_SIZE = 41
platform_img = pygame.image.load('Tiles/platform.png').convert_alpha()
platform_img = pygame.transform.scale(platform_img, (TILE_SIZE, TILE_SIZE/2))
def get_menu_platform_plan(platform_img):
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
        "x_start": 500,
        "y_start": 380,
        "count": 4,
        "images": [platform_img],
        "spawned": False,
    },
    {
        "x_start": 0,
        "y_start": 580,
        "count": 20,
        "images": [platform_img],
        "spawned": False,
    },
]
