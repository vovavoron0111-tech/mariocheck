from Player_sprites import *
from Backdrop_sprites import *
from Level1 import *
def move_world(camera_dx):
    for sprite in world_sprites:
        sprite.rect.x -= camera_dx

    for sprite in background_sprites:
        sprite.move_with_camera(camera_dx)
def create_ground_column(
    world_x,
    world_offset,
    HEIGHT,
    TILE_SIZE,
    ground_img,
    ground1_img,
    PlatformClass,
    all_sprites,
    world_sprites,
    platforms,
):
    screen_x = world_x - world_offset
    ground_top = Platform(screen_x, HEIGHT - TILE_SIZE * 3, ground_img)
    ground_middle = Platform(screen_x, HEIGHT - TILE_SIZE * 2, ground_img)
    ground_bottom = Platform(screen_x, HEIGHT - TILE_SIZE, ground_img)
    all_sprites.add(ground_top, ground_middle, ground_bottom)
    world_sprites.add(ground_top, ground_middle, ground_bottom)
    platforms.add(ground_top, ground_middle, ground_bottom)
def ensure_ground(
        next_ground_x,
        world_offset,
        WIDTH,
        HEIGHT,
        TILE_SIZE,
        ground_img,
        ground1_img,
        PlatformClass,
        all_sprites,
        world_sprites,
        platforms,
):

    while next_ground_x < world_offset + WIDTH + TILE_SIZE * 3:
        create_ground_column(
            next_ground_x,
            world_offset,
            HEIGHT,
            TILE_SIZE,
            ground_img,
            ground1_img,
            PlatformClass,
            all_sprites,
            world_sprites,
            platforms,
        )
        next_ground_x += TILE_SIZE
    return next_ground_x
def create_platform(
        count,
        images,
        y_start,
        x_start,
        world_offset,
        TILE_SIZE,
        PlatformClass,
        all_sprites,
        world_sprites,
        platforms,
        ):
    created_platforms = []

    for i in range(count):
        image = images[i % len(images)]
        screen_x = x_start + i * TILE_SIZE - world_offset

        platform = PlatformClass(screen_x, y_start, image)

        all_sprites.add(platform)
        world_sprites.add(platform)
        platforms.add(platform)

        created_platforms.append(platform)

    return created_platforms
def spawn_platforms(
    get_platform_plan,
    world_offset,
    WIDTH,
    spawn_distance,
    TILE_SIZE,
    PlatformClass,
    all_sprites,
    world_sprites,
    platforms,
):
    for platform_data in get_platform_plan():
        if not platform_data["spawned"]:
            if platform_data["x_start"] < world_offset + WIDTH + spawn_distance:
                create_platform(
                    platform_data["count"],
                    platform_data["images"],
                    platform_data["y_start"],
                    platform_data["x_start"],
                    world_offset,
                    TILE_SIZE,
                    PlatformClass,
                    all_sprites,
                    world_sprites,
                    platforms,
                )
                platform_data["spawned"] = True

def create_coin(
    world_x,
    y,
    radius,
    images,
    world_offset,
    CoinClass,
    all_sprites,
    world_sprites,
    coins,


):
    screen_x = world_x - world_offset
    coin = CoinClass(screen_x, y, radius, images)
    all_sprites.add(coin)
    world_sprites.add(coin)
    coins.add(coin)
    return coin
def spawn_coins(
    coin_plan,
    world_offset,
    WIDTH,
    spawn_distance,
    CoinClass,
    all_sprites,
    world_sprites,
    coins
):
    for coin_data in get_coin_plan():
        if not coin_data["spawned"]:
            if coin_data["x_start"] < world_offset + WIDTH + spawn_distance:
                create_coin(
                    coin_data["x_start"],
                    coin_data["y_start"],
                    coin_data["radius"],
                    coin_data["images"],
                    world_offset,
                    CoinClass,
                    all_sprites,
                    world_sprites,
                    coins
                )
                coin_data["spawned"] = True
def create_enemies(world_x, bottom_y, speed, world_offset, gravity, EnemyClass,
                   platforms, all_sprites, world_sprites, enemies):
    screen_x = world_x - world_offset
    enemy = EnemyClass(
        screen_x,
        bottom_y,
        platforms,
        speed,
        gravity,
    )
    all_sprites.add(enemy)
    world_sprites.add(enemy)
    enemies.add(enemy)
    return enemy

def spawn_enemies(
        enemie_plan,
        world_offset,
        WIDTH,
        spawn_distance,
        gravity,
        EnemyClass,
        platforms,
        all_sprites,
        world_sprites,
        enemies,
):
    for enemy_data in enemy_plan:
        if not enemy_data["spawned"]:
            if enemy_data["x"] < world_offset + WIDTH + spawn_distance:
                create_enemies(
                    enemy_data["x"],
                    enemy_data["bottom_y"],
                    enemy_data["speed"],
                    world_offset,
                    gravity,
                    EnemyClass,
                    platforms,
                    all_sprites,
                    world_sprites,
                    enemies,
                )
                enemy_data["spawned"] = True