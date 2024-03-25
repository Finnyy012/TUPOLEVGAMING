import pygame
import random
import agent
import balloon
import ground
import numpy as np
import settings
import matplotlib.pyplot as plt
import bulletv2 as bullet

import utilsv2 as utils
screen, font = None, None
if settings.USE_GUI:
    pygame.init()
    screen = pygame.display.set_mode(size=settings.SCREEN_RESOLUTION, flags=pygame.SRCALPHA)
    font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
running = True
dt = 0 
total_time = 0
fov_radius = 150

plane_1_data = settings.PLANE_POLIKARPOV_I_16
player = agent.Agent(
    settings.SCREEN_RESOLUTION,
    plane_1_data["SPRITE"],
    plane_1_data["MASS"],
    plane_1_data["ENGINE_FORCE"],
    plane_1_data["AGILITY"],
    plane_1_data["C_DRAG"],
    plane_1_data["C_LIFT"],
    plane_1_data["AOA_CRIT_LOW"],
    plane_1_data["AOA_CRIT_HIGH"],
    plane_1_data["CL0"],
    plane_1_data["CD_MIN"],
    plane_1_data["INIT_THROTTLE"],
    plane_1_data["INIT_PITCH"],
    plane_1_data["INIT_V"],
    plane_1_data["INIT_POS"],
)

floor = ground.Ground(
    height=50, 
    elevation=600, 
    coll_elevation=635,
)
if settings.USE_GUI:
    floor = ground.Ground(
        height=50, 
        elevation=600, 
        coll_elevation=635,
        sprite="assets/environment.png",
        resolution=settings.SCREEN_RESOLUTION
    )

    # pygame.mixer.music.load("assets/Arise, Great Country!.mp3")
    # pygame.mixer.music.play(-1)
    flip = pygame.mixer.Sound("assets/Flip de beer intro-[AudioTrimmer.com].mp3")
    background = pygame.image.load("assets/background.png")
    background = pygame.transform.scale(
        background,
        settings.SCREEN_RESOLUTION
    )
balloons = []
bullets = []
while running and total_time <= settings.SIMULATION_RUNTIME:
    balloons = utils.create_targets(balloons, floor.coll_elevation)
    if settings.USE_GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("white")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if player.throttle < 100:
                player.throttle += dt*100
        if keys[pygame.K_s]:
            if player.throttle > 0:
                player.throttle -= dt*100
        if keys[pygame.K_a]:
            player.adjust_pitch(dt)
        if keys[pygame.K_d]:
            player.adjust_pitch(-dt)
        if keys[pygame.K_q]:
            player.flip()
            flip.play()

        if keys[pygame.K_j]:
            player.pos_real[0] -= 200*dt
        if keys[pygame.K_l]:
            player.pos_real[0] += 200*dt
        if keys[pygame.K_i]:
            player.pos_real[1] -= 200*dt
        if keys[pygame.K_k]:
            player.pos_real[1] += 200*dt
        if keys[pygame.K_SPACE]:
            bullets.append(bullet.Bullet(
                player.pos_virtual,
                player.pitch,
                floor.coll_elevation,
                settings.BULLET["SPRITE"])
            )
    fov = []
    for b in balloons:
        if(np.linalg.norm(b.coords - player.pos_virtual)<fov_radius):
            fov.append([b.coords[0], b.coords[1], 1])
    # No GUI needed for tick
    player.tick(dt, np.array(fov))

    if settings.USE_GUI:
        # Draw (blit) background, player, ground, 
        #  baloons, lines, and tekst
        screen.blit(background, (0, 0))
        screen.blit(player.rot_sprite, player.rot_rect)
        screen.blit(floor.sprite, [0, floor.elevation])

        for plastic_orb in balloons:
            screen.blit(
                plastic_orb.sprite, plastic_orb.coords
            )
            colour="black"
            if(np.linalg.norm(plastic_orb.coords - player.pos_virtual)<fov_radius):
                colour = "green"
            screen.blit(
                font.render(
                    str(np.linalg.norm(plastic_orb.coords - player.pos_virtual)),
                    False,
                    colour
                ),
                plastic_orb.coords
            )

        center = np.array(
            (screen.get_width() / 2, screen.get_height() / 2)
        )

        pygame.draw.circle(surface=screen,color=0,center=player.pos_virtual,radius=fov_radius,width=2)

        pygame.draw.line(screen, "black", center, center + player.v)
        pygame.draw.line(
            screen, 
            "red", 
            center, 
            center + (player.f_engine) / 100
        )
        pygame.draw.line(
            screen, 
            "green", 
            center, 
            center + (player.f_lift) / 100
        )
        pygame.draw.line(
            screen, 
            "blue", 
            center, 
            center + (player.f_drag) / 100
        )
        pygame.draw.line(
            screen, 
            "yellow", 
            center, 
            center + (player.f_gravity) / 100
        )
        screen.blit(
            font.render(
                "throttle: " + str(player.throttle),
                False,
                "black"
            ),
            (20, 20)
        )
        screen.blit(
            font.render(
                "pitch:    " + str(player.pitch),
                False,
                "black"
            ),
            (20, 40)
        )
        screen.blit(
            font.render(
                "IAS M/S: " + str(np.linalg.norm(player.v)),
                False,
                "black"
            ),
            (20, 60)
        )
        screen.blit(
            font.render(
                "IAS KPH: " + str(np.linalg.norm(player.v)*3.6),
                False,
                "black"
            ),
            (20, 80)
        )
        screen.blit(
            font.render(
                "altitude: " + str(player.pos_real[1]),
                False,
                "black"
            ),
            (20, 100)
        )
        screen.blit(
            font.render(
                "AoA: " + str(player.AoA_deg),
                False,
                "black"
            ),
            (20, 120)
        )
        screen.blit(
            font.render(
                "test: " + str(player.testv3),
                False,
                "black"
            ),
            (20, 140)
        )
        screen.blit(
            font.render(
                "test: " + str(player.testv2),
                False,
                "black"
            ),
            (20, 160)
        )
        screen.blit(
            font.render(
                "d: " + str(player.nearest_target_pos_abs),
                False,
                "black"
            ),
            (20, 180)
        )
        utils.display_targets(balloons, screen)
        utils.display_projectiles(bullets, screen)
        utils.hit_detection_and_move_projectiles(bullets, balloons, dt)
        if utils.hit_collision_player(balloons, player) or \
           player.rot_rect.bottom >= floor.coll_elevation:
            running = False

        # Update display with current information
        pygame.display.flip()


    # Check if player has crashed onto the ground
    # if player.rot_rect.bottom >= floor.coll_elevation:
    #     running = False

    dt = clock.tick(settings.FPS) / 1000
    total_time += dt

if settings.USE_GUI:
    screen.fill((255,255,255))
    gameover = pygame.image.load("assets/gameover.png")
    r = gameover.get_rect()
    r.centerx = screen.get_width() / 2
    r.centery = screen.get_height() / 2
    screen.blit(gameover, r)

    explosion = pygame.transform.scale(
        pygame.image.load("assets/explosion2.png"), 
        (64,64)
    )
    explosion_rect = explosion.get_rect()
    explosion_rect.centerx = player.rot_rect.centerx
    explosion_rect.bottom = player.rot_rect.bottom
    screen.blit(explosion, explosion_rect)
    screen.blit(source=floor.sprite, dest=[0,floor.elevation])
    
    # Update display with current information
    pygame.display.flip()

    # Let the user enjoy the gameover screen for a second
    pygame.time.wait(2000)


pygame.quit()

plt.imshow(player.history[0].T)
plt.show()

appels = (np.where(player.history[1]==1))
for i in range(len(appels[0])):
    for x in range(3):
        for y in range(3):
            player.history[1][appels[0][i]-1+x][appels[1][i]-1+y] = 1


plt.imshow(player.history[1].astype(bool))
plt.show()

plt.imshow(player.history[0].T + (player.history[1].T * 60))
plt.show()



