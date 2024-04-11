import pygame
import numpy as np
import settings
import matplotlib.pyplot as plt

import bullet
from agent import Agent
import ground
import utils


plane_1_data = settings.PLANE_MESSERSCHMIDT_109E
plane_2_data = settings.PLANE_POLIKARPOV_I_16

floor = ground.Ground(
    height=50,
    elevation=600,
    coll_elevation=635,
)


dt = 0
total_time = 0
fov_radius = 150


for _ in range(settings.BATCH_SIZE):
    agent1 = Agent(
        settings.SCREEN_RESOLUTION,
        plane_2_data["SPRITE"],
        plane_2_data["SPRITE_TOP"],
        plane_2_data["MASS"],
        plane_2_data["ENGINE_FORCE"],
        plane_2_data["AGILITY"],
        plane_2_data["C_DRAG"],
        plane_2_data["C_LIFT"],
        plane_2_data["AOA_CRIT_LOW"],
        plane_2_data["AOA_CRIT_HIGH"],
        plane_2_data["CL0"],
        plane_2_data["CD_MIN"],
        plane_2_data["INIT_THROTTLE"],
        plane_2_data["INIT_PITCH"],
        plane_2_data["INIT_V"],
        plane_2_data["INIT_POS"],
    )

    agent2 = Agent(
        settings.SCREEN_RESOLUTION,
        plane_2_data["SPRITE"],
        plane_2_data["SPRITE_TOP"],
        plane_2_data["MASS"],
        plane_2_data["ENGINE_FORCE"],
        plane_2_data["AGILITY"],
        plane_2_data["C_DRAG"],
        plane_2_data["C_LIFT"],
        plane_2_data["AOA_CRIT_LOW"],
        plane_2_data["AOA_CRIT_HIGH"],
        plane_2_data["CL0"],
        plane_2_data["CD_MIN"],
        plane_2_data["INIT_THROTTLE"],
        plane_2_data["INIT_PITCH"],
        plane_2_data["INIT_V"],
        (1280 / 8, 250),
    )

    agent3 = Agent(
        settings.SCREEN_RESOLUTION,
        plane_1_data["SPRITE"],
        plane_1_data["SPRITE_TOP"],
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
        (1280 / 4, 250),
    )

    agent4 = Agent(
        settings.SCREEN_RESOLUTION,
        plane_1_data["SPRITE"],
        plane_1_data["SPRITE_TOP"],
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
        (1280 / 2, 250),
    )

    screen, font = None, None
    if settings.USE_GUI:
        pygame.init()
        screen = pygame.display.set_mode(
            size=settings.SCREEN_RESOLUTION,
            flags=pygame.SRCALPHA
        )
        font = pygame.font.SysFont(None, 24)

        floor = ground.Ground(
            height=settings.GROUND["HEIGHT"], 
            elevation=settings.GROUND["ELEVATION"],
            coll_elevation=settings.GROUND["COLL_ELEVATION"],
            sprite=settings.GROUND["SPRITE"],
            resolution=settings.SCREEN_RESOLUTION
        )

        pygame.mixer.music.load("assets/Arise, Great Country!.mp3")
        pygame.mixer.music.play(-1)
        flip = pygame.mixer.Sound(
            "assets/Flip de beer intro-[AudioTrimmer.com].mp3"
        )
        background = pygame.image.load("assets/background.png")
        background = pygame.transform.scale(
            background,
            settings.SCREEN_RESOLUTION
        )
        
    clock = pygame.time.Clock()
    # agents = [agent1, agent2, agent3, agent4]
    agents = [agent1]
    targets = []
    targets = utils.create_targets(targets, floor.coll_elevation)
    running = True
    while running and total_time <= settings.SIMULATION_RUNTIME:
        # if respawning needs to be disabled, place the following line
        # outside the while loop
        if settings.USE_GUI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    # This block runs when a key is released
                    if event.key == pygame.K_SPACE:
                        agent1.shoot()

            screen.fill("white")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                if agent1.throttle < 100:
                    agent1.throttle += dt * 100
            if keys[pygame.K_s]:
                if agent1.throttle > 0:
                    agent1.throttle -= dt * 100
            if keys[pygame.K_a]:
                agent1.adjust_pitch(dt)
            if keys[pygame.K_d]:
                agent1.adjust_pitch(-dt)
            if keys[pygame.K_q]:
                agent1.flip()
                flip.play()

            if keys[pygame.K_j]:
                agent1.pos_real[0] -= 200 * dt
            if keys[pygame.K_l]:
                agent1.pos_real[0] += 200 * dt
            if keys[pygame.K_i]:
                agent1.pos_real[1] -= 200 * dt
            if keys[pygame.K_k]:
                agent1.pos_real[1] += 200 * dt

        agent11_fov = utils.check_surround(
            agent1,
            targets,
            agents,
            fov_radius
        )
        agent2_fov = utils.check_surround(
            agent2,
            targets,
            agents,
            fov_radius
        )
        agent3_fov = utils.check_surround(
            agent3,
            targets,
            agents,
            fov_radius
        )
        agent14_fov = utils.check_surround(
            agent4,
            targets,
            agents,
            fov_radius
        )

        fov_list = [agent11_fov, agent2_fov, agent3_fov, agent14_fov]

        agent1.target = targets[0].coords

        for x, agent in enumerate(agents):
            agent.tick(dt, np.array(fov_list[x]))

        utils.hit_detection_agents(agents)
        # No GUI needed for tick
        for agent in agents:
            utils.hit_detection_and_move_projectiles(
                targets,
                agents,
                agent,
                dt
            )
            if utils.hit_collision_agents(targets, agent) or \
                    agent.rot_rect.bottom >= floor.coll_elevation:
                agents.remove(agent)
                print("agent crashed")

        if settings.USE_GUI:
            # Draw (blit) background, agent1, ground,
            #  baloons, lines, and tekst
            screen.blit(background, (0, 0))

            for agent in agents:
                screen.blit(agent.rot_sprite, agent.rot_rect)
            screen.blit(floor.sprite, [0, floor.elevation])

            for target in targets:
                screen.blit(
                    target.sprite, target.coords
                )
                colour = "black"
                if (
                        np.linalg.norm(
                            target.coords - agent1.pos_virtual
                        ) < fov_radius
                ):
                    colour = "green"
                screen.blit(
                    font.render(
                        str(
                            np.linalg.norm(
                                target.coords -
                                agent1.pos_virtual
                            )
                        ),
                        False,
                        colour
                    ),
                    target.coords
                )

            center = np.array(
                (screen.get_width() / 2, screen.get_height() / 2)
            )

            pygame.draw.circle(
                surface=screen,
                color=0,
                center=agent1.pos_virtual,
                radius=fov_radius,
                width=2
            )

            pygame.draw.line(screen, "black", center, center + agent1.v)
            pygame.draw.line(
                screen,
                "red",
                center,
                center + (agent1.f_engine) / 100
            )
            pygame.draw.line(
                screen,
                "green",
                center,
                center + (agent1.f_lift) / 100
            )
            pygame.draw.line(
                screen,
                "blue",
                center,
                center + (agent1.f_drag) / 100
            )
            pygame.draw.line(
                screen,
                "yellow",
                center,
                center + (agent1.f_gravity) / 100
            )
            screen.blit(
                font.render(
                    "throttle: " + str(agent1.throttle),
                    False,
                    "black"
                ),
                (20, 20)
            )
            screen.blit(
                font.render(
                    "pitch:    " + str(agent1.pitch),
                    False,
                    "black"
                ),
                (20, 40)
            )
            screen.blit(
                font.render(
                    "IAS M/S: " + str(np.linalg.norm(agent1.v)),
                    False,
                    "black"
                ),
                (20, 60)
            )
            screen.blit(
                font.render(
                    "IAS KPH: " + str(np.linalg.norm(agent1.v) * 3.6),
                    False,
                    "black"
                ),
                (20, 80)
            )
            screen.blit(
                font.render(
                    "altitude: " + str(agent1.pos_real[1]),
                    False,
                    "black"
                ),
                (20, 100)
            )
            screen.blit(
                font.render(
                    "AoA: " + str(agent1.AoA_deg),
                    False,
                    "black"
                ),
                (20, 120)
            )
            screen.blit(
                font.render(
                    "test: " + str(agent1.testv3),
                    False,
                    "black"
                ),
                (20, 140)
            )
            screen.blit(
                font.render(
                    "test: " + str(agent1.testv2),
                    False,
                    "black"
                ),
                (20, 160)
            )
            screen.blit(
                font.render(
                    "d: " + str(agent1.nearest_target_pos_abs),
                    False,
                    "black"
                ),
                (20, 180)
            )
            # utils.display_targets(targets, screen)
            utils.display_projectiles(agents, screen)
            pygame.display.flip()

        if not agents or not targets:
            running = False
        # Update display with current information

        dt = clock.tick(settings.FPS) / 1000
        total_time += dt

    if settings.USE_GUI:
        screen.fill((255, 255, 255))
        gameover = pygame.image.load("assets/gameover.png")
        r = gameover.get_rect()
        r.centerx = screen.get_width() / 2
        r.centery = screen.get_height() / 2
        screen.blit(gameover, r)

        explosion = pygame.transform.scale(
            pygame.image.load("assets/explosion2.png"),
            (64, 64)
        )
        explosion_rect = explosion.get_rect()
        explosion_rect.centerx = agent1.rot_rect.centerx
        explosion_rect.bottom = agent1.rot_rect.bottom
        screen.blit(explosion, explosion_rect)
        screen.blit(source=floor.sprite, dest=[0, floor.elevation])

        # Update display with current information
        pygame.display.flip()

        # Let the user enjoy the gameover screen for a second
        pygame.time.wait(2000)
    else:
        print(f"agents remaining: {len(agents)}")
        print(f"targets remaining: {len(targets)}")
        print("game is done")

    pygame.quit()

# plt.imshow(agent1.history[0].T)
# plt.show()

# appels = (np.where(agent1.history[1] == 1))
# for i in range(len(appels[0])):
#     for x in range(3):
#         for y in range(3):
#             agent1.history[1][appels[0][i] - 1 + x][appels[1][i] - 1 + y] = 1

# plt.imshow(agent1.history[1].astype(bool))
# plt.show()

# plt.imshow(agent1.history[0].T + (agent1.history[1].T * 60))
# plt.show()