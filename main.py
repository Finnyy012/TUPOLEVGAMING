import pygame
import numpy as np
import settings
import matplotlib.pyplot as plt

from agent import Agent
from team import Team
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

plane_1_data = settings.PLANE_MESSERSCHMIDT_109E
plane_2_data = settings.PLANE_POLIKARPOV_I_16
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

# agents = [agent1]
agentsforteam = [agent1, agent2, agent3, agent4]
agentsall = [agent1, agent2, agent3, agent4]

team1 = Team(copy.deepcopy(targetscoords), agentsforteam)

teams = [team1]
while running and total_time <= settings.SIMULATION_RUNTIME:
    # if respawning needs to be disabled, place the following line
    # outside the while loop
    
    if settings.USE_GUI:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill("white")

    for team in teams:
        fov_list = [utils.check_surround(agent, targets, agentsall, fov_radius) for agent in team.agents]

        for x, agent in enumerate(team.agents):
            agent.tick(dt, np.array(fov_list[x]))

        utils.hit_detection_agents(agentsall)

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
                print("--------------------------------")
                print(len(team.targets))
                utils.hit_detection_and_move_projectiles(
                    targets,
                    agentsall,
                    agent,
                    dt
                )
                print(len(team.targets))
                if utils.hit_collision_agents(targets, agent) or \
                        agent.rot_rect.bottom >= floor.coll_elevation:
                    team.agents.remove(agent)
                    agentsall.remove(agent)

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
    explosion_rect.centerx = agent1.rot_rect.centerx
    explosion_rect.bottom = agent1.rot_rect.bottom
    screen.blit(explosion, explosion_rect)
    screen.blit(source=floor.sprite, dest=[0, floor.elevation])

    # Update display with current information
    pygame.display.flip()

    # Let the user enjoy the gameover screen for a second
    pygame.time.wait(2000)

pygame.quit()

