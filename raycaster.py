"""
A raycaster made in Pygame that I pulled together by relying on various resources. As of now it has poor performance due to unoptimised code. 
I will learn the proper way of doing things soon.

It uses the DDA algorithm for detecting collisions against walls.
"""

import pygame, sys, math
from pygame import Vector2

# UNBELIEVABLY HORRIBLE PERFORMANCE
pygame.init()
pygame.font.init()

SCREEN_RES = 800
TILE_SIZE = 50

RAY_COUNT = 800

TILES = [[0 for x in range(SCREEN_RES//TILE_SIZE)] for x in range(SCREEN_RES//TILE_SIZE)]

display = pygame.display.set_mode((SCREEN_RES, SCREEN_RES))
font = pygame.font.Font()
clock = pygame.time.Clock()


SPEED = 150
SIZE = (20, 20)
pos = Vector2(400, 400)
velocity = Vector2(0, 0)
player_direction = 180
FOV = 60
ANGLE_INCREMENT = FOV/RAY_COUNT

left = False
right = False
up = False
down = False
shift = False
render = False  # When true, we render the 3D environment. When false, we render the map.

rotate_l = False
rotate_r = False
angular_speed = 360/2

delta_time = 1/60

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_w:
                up = True

            elif event.key == pygame.K_s:
                down = True

            elif event.key == pygame.K_a:
                left = True

            elif event.key == pygame.K_d:
                right = True
            
            elif event.key == pygame.K_LSHIFT:
                shift = True

            elif event.key == pygame.K_j:
                rotate_l = True

            elif event.key == pygame.K_l:
                rotate_r = True

            elif event.key == pygame.K_LCTRL:
                render = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False

            elif event.key == pygame.K_s:
                down = False

            elif event.key == pygame.K_a:
                left = False

            elif event.key == pygame.K_d:
                right = False
            
            elif event.key == pygame.K_LSHIFT:
                shift = False

            elif event.key == pygame.K_j:
                rotate_l = False

            elif event.key == pygame.K_l:
                rotate_r = False

            elif event.key == pygame.K_LCTRL:
                render = False
        
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    dir_vector = Vector2(math.cos(math.radians(player_direction)), math.sin(math.radians(player_direction)))
    left_vector = Vector2(dir_vector.y, -dir_vector.x)
    final_direction = Vector2(0, 0)

    if left:
        final_direction += left_vector
    if right:
        final_direction += -left_vector
    if up:
        final_direction += dir_vector
    if down:
        final_direction += -dir_vector

    velocity = final_direction * SPEED
    if not left and not right and not up and not down and velocity.length() != 0:
        velocity = Vector2(0, 0)

    pos.x += velocity.x * delta_time
    pos.y += velocity.y * delta_time

    if rotate_l:
        player_direction -= angular_speed * delta_time
        if player_direction < 0:
            player_direction = 360
    elif rotate_r:
        player_direction += angular_speed * delta_time

        if player_direction >= 360:
            player_direction = 0

    display.fill((255, 255, 255))

    if not render:  # Render the tile map
        for y, row in enumerate(TILES):
            for x, tile in enumerate(row):
                if tile == 1:
                    tile_pos = (x * TILE_SIZE, y * TILE_SIZE)
                    pygame.draw.rect(display, (0, 0, 255), pygame.Rect(tile_pos[0], tile_pos[1], TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    tile_pos = (x * TILE_SIZE, y * TILE_SIZE)
                    pygame.draw.rect(display, (200, 200, 0), pygame.Rect(tile_pos[0], tile_pos[1], TILE_SIZE, TILE_SIZE))

        for i in range(SCREEN_RES//TILE_SIZE):
            pygame.draw.line(display, (0, 0, 0), Vector2(i * TILE_SIZE, 0), Vector2(i * TILE_SIZE, SCREEN_RES), 1)
            pygame.draw.line(display, (0, 0, 0), Vector2(0, i * TILE_SIZE), Vector2(SCREEN_RES, i * TILE_SIZE), 1)


        # Drawing player
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(pos.x - SIZE[0]/2, pos.y - SIZE[1]/2, SIZE[0] - 1, SIZE[1] - 1))

        # Drawing line to represent player's direction.
        pygame.draw.line(display, (150, 10, 150), pos, pos + dir_vector*20) 


    # Input-handling code for adding and removing walls
    left_clicked, middle_clicked, right_clicked = pygame.mouse.get_pressed()
    if right_clicked and not shift:
        click_pos = pygame.mouse.get_pos()
        nearest_x = click_pos[0]//TILE_SIZE
        nearest_y = click_pos[1]//TILE_SIZE

        if TILES[nearest_y][nearest_x] != 1:
            TILES[nearest_y][nearest_x] = 1

    elif shift and right_clicked:
        click_pos = pygame.mouse.get_pos()
        nearest_x = click_pos[0]//TILE_SIZE
        nearest_y = click_pos[1]//TILE_SIZE

        if TILES[nearest_y][nearest_x] != 0:
            TILES[nearest_y][nearest_x] = 0

    # The DDA algorithm used for raycasting
    for i in range(RAY_COUNT):
        direction_angle = player_direction - FOV/2 + ANGLE_INCREMENT * i  # Direction of the ray
        if direction_angle > 360:
            direction_angle = direction_angle - 360
        elif direction_angle < 0:
            direction_angle = 360 + direction_angle

        direction = Vector2(math.cos(math.radians(direction_angle)), math.sin(math.radians(direction_angle)))

        ray_start = pos
        ray_unit_step_size = Vector2()
        if direction[0] != 0:
            ray_unit_step_size.x = math.sqrt(TILE_SIZE**2 + (TILE_SIZE * direction[1]/direction[0])**2)
        else:
            ray_unit_step_size.x = float("inf")
        
        if direction[1] != 0:
            ray_unit_step_size.y = math.sqrt(TILE_SIZE**2 + (TILE_SIZE * direction[0]/direction[1])**2)
        else:
            ray_unit_step_size.y = float("inf")

        map_check = Vector2((pos.x//TILE_SIZE) * TILE_SIZE, (pos.y//TILE_SIZE) * TILE_SIZE)

        ray_length_1d = Vector2(0, 0)
        step = Vector2(0, 0)

        if direction.x < 0:
            step.x = -TILE_SIZE
            ray_length_1d.x = (ray_start.x - map_check.x)/TILE_SIZE * ray_unit_step_size.x
        else:
            step.x = TILE_SIZE
            ray_length_1d.x = (map_check.x + TILE_SIZE - ray_start.x)/TILE_SIZE * ray_unit_step_size.x

        if direction.y < 0:
            step.y = -TILE_SIZE
            ray_length_1d.y = (ray_start.y - map_check.y)/TILE_SIZE * ray_unit_step_size.y
        else:
            step.y = TILE_SIZE
            ray_length_1d.y = (map_check.y + TILE_SIZE - ray_start.y)/TILE_SIZE * ray_unit_step_size.y

        collision_found = False
        distance = 0
        while not collision_found and map_check.x < SCREEN_RES and map_check.y < SCREEN_RES and map_check.x >= 0 and map_check.y >= 0:
            if ray_length_1d.x < ray_length_1d.y:
                map_check.x += step.x
                distance = ray_length_1d.x
                ray_length_1d.x += ray_unit_step_size.x
            else:
                map_check.y += step.y
                distance = ray_length_1d.y
                ray_length_1d.y += ray_unit_step_size.y
            

            if map_check.x < SCREEN_RES and map_check.x >= 0 and map_check.y < SCREEN_RES and map_check.y >= 0:
                map_pos_x = int(map_check.x//TILE_SIZE)
                map_pos_y = int(map_check.y//TILE_SIZE)

                if TILES[map_pos_y][map_pos_x] in [1, 2]:
                    TILES[map_pos_y][map_pos_x] = 2
                    collision_found = True

        if render:
            if collision_found:
                p = distance * math.cos(math.radians(abs(player_direction - direction_angle)))
                # p represents the perpendicular distance to the camera plane instead of the direct distance between player and plane.
                # This prevents the fisheye effect.
                height = 50000/p
                pygame.draw.line(display, (0, 0, 255), (i, SCREEN_RES/2 - height/2), (i, SCREEN_RES/2 + height/2), 1)
    

    fps = clock.get_fps()
    if fps != 0:
        delta_time = 1/fps

    fps_text = font.render(str(int(fps)), True, (50, 50, 50))
    display.blit(fps_text, (0, 0))

    pygame.display.update()
    clock.tick(1500)