from itertools import chain
import pygame
import numpy as np
import settings
import matplotlib.pyplot as plt

from absolute_distance_team import AbsolteDistanceTeam
import ground
import utils
import copy

screen, font = None, None
if settings.USE_GUI:
    pygame.init()
    screen = pygame.display.set_mode(
        size=settings.SCREEN_RESOLUTION,
        flags=pygame.SRCALPHA
    )
    font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
running = True
dt = 0
total_time = 0
fov_radius = 150

floor = ground.Ground(
    height=settings.GROUND["HEIGHT"],
    elevation=settings.GROUND["ELEVATION"],
    coll_elevation=settings.GROUND["COLL_ELEVATION"],
)
if settings.USE_GUI:
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

targets = []

targets = utils.create_targets(targets, floor.coll_elevation)
targetscoords = np.array([target.coords for target in targets])

team1 = AbsolteDistanceTeam(
    copy.deepcopy(targetscoords),
    2, 
    settings.PLANE_POLIKARPOV_I_16, 
    0
)

team2 = AbsolteDistanceTeam(
    copy.deepcopy(targetscoords),
    4, 
    settings.PLANE_POLIKARPOV_I_16, 
    1
)

teams = [team1, team2]
agents_all = list(chain(*[team.agents for team in teams]))

while running and total_time <= settings.SIMULATION_RUNTIME:
    
    if settings.USE_GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill("white")

    for team in teams:
        fov_list = [utils.check_surround(agent, targets, agents_all, fov_radius) for agent in team.agents]
        team.assign_targets()
        for x, agent in enumerate(team.agents):
            agent.tick(dt, np.array(fov_list[x]))

        utils.hit_detection_agents(agents_all)

    if settings.USE_GUI:
        # Draw (blit) background, agent1, ground,
        #  baloons, lines, and tekst
        screen.blit(background, (0, 0))
        
        for team in teams:
            for agent in team.agents:
                screen.blit(agent.rot_sprite, agent.rot_rect)
        screen.blit(floor.sprite, [0, floor.elevation])

        utils.display_targets(targets, screen)
        for team in teams:
            utils.display_projectiles(team.agents, screen)

        for team in teams:
            for agent in team.agents:
                # print("--------------------------------")
                # print(len(team.targets))
                utils.hit_detection_and_move_projectiles(
                    targets,
                    agents_all,
                    agent,
                    dt
                )
                # print(len(team.targets))
                if utils.hit_collision_agents(targets, agent) or \
                        agent.rot_rect.bottom >= floor.coll_elevation:
                    team.agents.remove(agent)
                    agents_all.remove(agent)

        # Update display with current information
        pygame.display.flip()

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
    explosion_rect.centerx = agents_all[0].rot_rect.centerx # NOTE: THIS SHOULDNT BE THE FIRST AGENT BUT THE ONE EXPLODING.
    explosion_rect.bottom = agents_all[0].rot_rect.bottom
    screen.blit(explosion, explosion_rect)
    screen.blit(source=floor.sprite, dest=[0, floor.elevation])

    # Update display with current information
    pygame.display.flip()

    # Let the user enjoy the gameover screen for a second
    pygame.time.wait(2000)

pygame.quit()

