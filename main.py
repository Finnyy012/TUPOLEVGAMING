import numpy as np
import pygame
import aircraft
import environment
import settings

screen, font = None, None
if settings.USE_GUI:
    pygame.init()
    screen = pygame.display.set_mode(settings.SCREEN_RESOLUTION)
    font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
running = True
dt = 0
total_time = 0 # in seconds


plane_1_data = settings.PLANE_POLIKARPOV_I_16
player = aircraft.Aircraft(
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
environment = environment.Environment("assets/environment.png", (screen.get_width(), screen.get_height()), 100, 200, 200)

while running and total_time <= settings.SIMULATION_RUNTIME:
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

    # No GUI needed for tick
    player.tick(dt)

    if settings.USE_GUI:
        screen.blit(player.rot_sprite, player.rot_rect)

        center = np.array((screen.get_width() / 2, screen.get_height() / 2))
        pygame.draw.line(screen, "black", center, center + player.v)
        pygame.draw.line(screen, "red", center, center + (player.f_engine)/100)
        pygame.draw.line(screen, "green", center, center + (player.f_lift)/100)
        pygame.draw.line(screen, "blue", center, center + (player.f_drag)/100)
        pygame.draw.line(screen, "yellow", center, center + (player.f_gravity)/100)

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
                "altitude: " + str(player.pos[1]),
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

        pygame.display.flip()

    # No GUI needed for clock
    dt = clock.tick(settings.FPS) / 1000
    total_time += dt

pygame.quit()
