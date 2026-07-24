import pygame
import random
from Player_sprites import *
from Backdrop_sprites import *
from Level1 import *
from World_update_fun import *


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
enemy_spawn_distance = 50
font = pygame.font.SysFont('arial', 36)
big_font = pygame.font.SysFont('arial', 72, bold=True)

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





sky1 = BackgroundSprite(0, 0, WIDTH, HEIGHT,  0.05, sky_blue)
sky2 = BackgroundSprite(WIDTH, 0, WIDTH, HEIGHT,  0.05, sky_blue)
hill1 = Hill(0, 360, 0.25)
hill2 = Hill(500, 370, 0.25)
hill3 = Hill(1000, 350, 0.25)
cloud1 = Cloud(100, 80, 0.4)
cloud2 = Cloud(450, 140, 0.4)
cloud3 = Cloud(850, 90, 0.4)

player = Player(
    player_idle_right,
    player_idle_left,
    player_walk_right,
    player_walk_left,
    player_jump_right,
    player_jump_left,
)
platform_plan = get_platform_plan(platform_img)
coin_plan = get_coin_plan(coin_images_original)
enemy_plan = get_enemy_plan(HEIGHT, TILE_SIZE)




platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
world_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()


all_sprites.add(player)
all_sprites.add(platforms)
background_sprites.add(
    sky1,
    sky2,
    hill1,
    hill2,
    hill3,
    cloud1,
    cloud2,
    cloud3
)

next_ground_x = ensure_ground(
    next_ground_x,
    world_offset,
    WIDTH,
    HEIGHT,
    TILE_SIZE,
    ground_img,
    ground1_img,
    Platform,
    all_sprites,
    world_sprites,
    platforms,
)

spawn_platforms(
    get_platform_plan,
    world_offset,
    WIDTH,
    spawn_distance,
    TILE_SIZE,
    Platform,
    all_sprites,
    world_sprites,
    platforms,
)
spawn_coins(
    get_coin_plan,
    world_offset,
    WIDTH,
    spawn_distance,
    Coin,
    all_sprites,
    world_sprites,
    coins
)
spawn_enemies(
    enemy_plan,
    world_offset,
    WIDTH,
    enemy_spawn_distance,
    gravity,
    Enemy,
    platforms,
    all_sprites,
    world_sprites,
    enemies,
)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()

    #-----#
    if player.rect.centerx > camera_border_x:
        camera_dx = player.rect.centerx - camera_border_x
        player.rect.centerx = camera_border_x
        world_offset += camera_dx
        move_world(camera_dx)

    next_ground_x = ensure_ground(
        next_ground_x,
        world_offset,
        WIDTH,
        HEIGHT,
        TILE_SIZE,
        ground_img,
        ground1_img,
        Platform,
        all_sprites,
        world_sprites,
        platforms,
    )
    spawn_platforms(
        get_platform_plan,
        world_offset,
        WIDTH,
        spawn_distance,
        TILE_SIZE,
        Platform,
        all_sprites,
        world_sprites,
        platforms,
    )
    spawn_coins(
        get_coin_plan,
        world_offset,
        WIDTH,
        spawn_distance,
        Coin,
        all_sprites,
        world_sprites,
        coins
    )
    spawn_enemies(
        enemy_plan,
        world_offset,
        WIDTH,
        enemy_spawn_distance,
        gravity,
        Enemy,
        platforms,
        all_sprites,
        world_sprites,
        enemies,
    )



    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    for coin in  collected_coins:
        score += coin.price

    if pygame.sprite.spritecollide(player, enemies):
        game_over = True


    timer += 1
    screen.fill(white)
    background_sprites.draw(screen)
    all_sprites.draw(screen)

    score_text = font.render(f'Coins: {score}', True, black)
    time_text = font.render(f'Time: {timer}', True, black)
    distance_text = font.render(f'Distance: {int(world_offset)}', True, black)

    screen.blit(score_text, (20, 20))
    screen.blit(time_text, (500, 20))
    screen.blit(distance_text, (20, 60))


    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        game_over_text = big_font.render('GAME OVER', True, white)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
pygame.quit()