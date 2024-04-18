import time
from itertools import chain
import pygame
import numpy as np
import settings

from absolute_distance_team import AbsoluteDistanceTeam
from energy_bidding_team import EnergyBiddingTeam
from two_targets_distance_team import TwoTargetsTeam
from target import Target
import ground
import utils
import copy

start = time.time()

screen, font = None, None
if settings.USE_GUI:
    pygame.init()
    screen = pygame.display.set_mode(
        size=settings.SCREEN_RESOLUTION,
        flags=pygame.SRCALPHA
    )
    font = pygame.font.SysFont(None, 24)

total_scores = [0, 0]

for _ in range(settings.BATCH_SIZE):
    if settings.USE_GUI:
        clock = pygame.time.Clock()
        dt = 0
    else:
        dt = 1 / 60
    running = True
    total_time = 0
    fov_radius = 150

    plane_1_data = settings.PLANE_I_16_FALANGIST
    plane_2_data = settings.PLANE_I_16_REPUBLICAN

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

    team1 = AbsoluteDistanceTeam(
        copy.deepcopy(targetscoords),
        2, 
        settings.PLANE_I_16_REPUBLICAN,
        0
    )

    team2 = EnergyBiddingTeam(
        copy.deepcopy(targetscoords),
        2,
        settings.PLANE_I_16_FALANGIST,
        1
    )

    teams = [team1, team2]

    agents_all = list(chain(*[team.agents for team in teams]))

    while running and total_time <= settings.SIMULATION_RUNTIME:
        if len(targets) == 0 or len(agents_all) == 0:
            running = False
  
        if settings.USE_GUI:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            screen.fill("white")
        
        for team in teams:
            fov_list = [
                utils.check_surround(
                    agent, 
                    targets, 
                    agents_all, 
                    fov_radius
                ) for agent in team.agents
            ]

            team.assign_targets()
            team.calculate_score()
            for x, agent in enumerate(team.agents):
                agent_target = Target(
                    floor.coll_elevation,
                    settings.TARGET["SPRITE"]
                )
                agent_target.coords = np.array(agent.target)
                if agent.target is not None:
                    if utils.check_surround(
                        agent, 
                        [agent_target], 
                        [], 
                        fov_radius
                    ) != []:
                        if np.append(
                            agent.target, 
                            1
                        ).tolist() not in utils.check_surround(
                            agent, 
                            targets, 
                            [], 
                            fov_radius
                        ):
                            indices_to_remove = np.where(
                                np.all(
                                    team.targets == agent.target, 
                                    axis=1
                                )
                            )
                            team.targets = np.delete(
                                team.targets, 
                                indices_to_remove, 
                                axis=0
                            )
                agent.tick(dt, np.array(fov_list[x]))

        if settings.COLLISION:
            utils.hit_detection_agents(agents_all)
        dead_agents = []

        for team in teams:
            for agent in team.agents:
                dead_agents.append(utils.hit_detection_and_move_projectiles(
                        targets,
                        agents_all,
                        agent,
                        dt
                    )
                )

                if settings.COLLISION:
                    if agent.rot_rect.bottom >= floor.coll_elevation or \
                            utils.hit_collision_agents(targets, agent):
                        team.agents.remove(agent)

        if settings.USE_GUI:
            screen.blit(background, (0, 0))
            
            for team in teams:
                for agent in team.agents:
                    screen.blit(agent.rot_sprite, agent.rot_rect)
            screen.blit(floor.sprite, [0, floor.elevation])

            utils.display_targets(targets, screen)
            for team in teams:
                utils.display_projectiles(team.agents, screen)
                for agent in team.agents:
                    screen.blit(agent.rot_sprite, agent.rot_rect)
            screen.blit(floor.sprite, [0, floor.elevation])

            utils.display_targets(targets, screen)
            for team in teams:
                utils.display_projectiles(team.agents, screen)    
            for team in teams:
                team.agents = [
                    agent for agent in team.agents if agent not in dead_agents
                ]
                # Update display with current information
            pygame.display.flip()

        if settings.USE_GUI:
            dt = clock.tick(settings.FPS) / 1000

        total_time += dt

    if settings.USE_GUI:
        screen.fill((255, 255, 255))
        gameover = pygame.image.load(settings.END_SCREEN["GAMEOVER"])
        r = gameover.get_rect()
        r.centerx = screen.get_width() / 2
        r.centery = screen.get_height() / 2
        screen.blit(gameover, r)

        explosion = pygame.transform.scale(
            pygame.image.load(settings.END_SCREEN["EXPLOSION"]),
            settings.END_SCREEN["EXPLOSION_SIZE"]
        )
        explosion_rect = explosion.get_rect()

        explosion_rect.centerx = settings.SCREEN_RESOLUTION[0] / 2
        explosion_rect.centery = settings.SCREEN_RESOLUTION[1] / 2

        screen.blit(explosion, explosion_rect)
        screen.blit(source=floor.sprite, dest=[0, floor.elevation])

        # Update display with current information
        pygame.display.flip()

        # Let the user enjoy the gameover screen for 2 seconds
        pygame.time.wait(2000)
    else:
        for i, team in enumerate(teams):
            total_scores[i] += team.score
            print(team)
print(teams[0].__class__.__name__) 
print(f"\tThe first team scored {total_scores[0]} points \
over {settings.BATCH_SIZE} runs\n\tOn average they scored \
{total_scores[0] / settings.BATCH_SIZE} points per run\n"
)

print(teams[1].__class__.__name__)    
print(f"\tThe first team scored {total_scores[1]} points \
over {settings.BATCH_SIZE} runs\n\tOn average they scored \
{total_scores[1] / settings.BATCH_SIZE} points per run\n"
)

print(f"{total_scores[0] / settings.BATCH_SIZE}/\
{total_scores[1] / settings.BATCH_SIZE}"
)
pygame.quit()

print(f"The program took {round(time.time()-start, 2)} seconds to run.")
