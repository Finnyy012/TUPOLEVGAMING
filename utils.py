import settings
import pygame
import numpy as np
from itertools import compress
import agent
import aircraft
import bullet as bullet
import balloon


def hit_detection_and_move_projectiles(
        projectiles: bullet.Bullet,
        targets: balloon.Balloon, 
        agents: list[agent.Agent],
        agent: agent.Agent,
        dt: float
    ) -> None:
    """
    This function checks if a bullet hits a balloon or a plane.
    
    :param projectiles: list of bullets (list[bullet.Bullet])
    :param targets: list of balloons (list[balloon.Balloon])
    :param dt: time step (float)
    :return: None
    """


    for projectile in projectiles:
        if projectile.move_bullet(dt):
            projectiles.remove(projectile)
            continue
        for a in agents:
            if np.linalg.norm(np.array(a.rot_rect.center) - \
               np.array(projectile.rect.center)) <= 5 and a != agent:
                projectiles.remove(projectile)
                agents.remove(a)
                continue

        for orb in targets:
            if projectile.rect.colliderect(orb.rect):
                projectiles.remove(projectile)
                targets.remove(orb)
                continue
    
def hit_detection_agents(
        agents: list[agent.Agent],
    ) -> None:
    """
    This function checks if an agent hits another agent
    
    :param agents: list of agents (list[agent.Agent])
    :return: None
    """
    for agent1 in agents:
        for agent2 in agents:
            if agent1 != agent2:
                if np.linalg.norm(np.array(agent1.rot_rect.center) \
                - np.array(agent2.rot_rect.center) 
                ) < 24:
                    agents.remove(agent1)
                    agents.remove(agent2)
                
                
def hit_collision_player(
        targets: list[balloon.Balloon], 
        player: aircraft.Aircraft
    ) -> bool:
    """
    This function checks if the player hits a balloon. If a player
     hits a balloon, the function returns True.

    :param targets: list of balloons (list[Balloon])
    :param player: player object (aircraft.Aircraft)
    :return: bool
    """
    for target in targets:
        if np.linalg.norm(
            np.array(player.rot_rect.center) - target.rect.center
        ) < 10:
            return True
    return False
     
def create_targets(
        targets: list[balloon.Balloon], 
        ground_height: int
    ) -> list[balloon.Balloon]:
    """
    This function generates new targets if the number of targets is 
     less than the defined amount in settings.py. Ground height is used
     to spawn targets above the ground.
    
    :param targets: list of balloons (list[Balloon])
    :param ground_height: height of the ground (int)
    :return: list of balloons (list[Balloon])
    """
    if len(targets) < settings.BALLOON["BALLOON_COUNT"]:
        new_targets = balloon.load_single_type_balloons(
            ground_height,
            settings.BALLOON["BALLOON_COUNT"] - len(targets)
        )
        new_targets.extend(targets)
        return new_targets
    else:
        return targets


def display_targets(
        targets: list[balloon.Balloon], 
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the targets on the screen.
    
    :param targets: list of balloons (list[Balloon])
    :param screen: screen (pygame.Surface)
    :return: None
    """
    for plastic_orb in targets:
        screen.blit(
            plastic_orb.sprite, plastic_orb.coords
        )


def display_projectiles(
        agents: list[agent.Agent],
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the bullets on the screen.

    @Parameters:
    :param projectiles: list of bullets (list[bullet.Bullet])
    :param screen: screen (pygame.Surface)
    :return: None
    """
    for agent in agents:
        for bullet in agent.bullets:
            screen.blit(
                pygame.transform.flip(
                    bullet.sprite,
                    True, 
                    False
                    ), 
                bullet.coords
            )


def check_surround(
        player: agent.Agent, 
        balloons: list[balloon.Balloon], 
        agents : list[agent.Agent],
        fov_radius: int
    ) -> list: 
    """
    This function checks the surrounding of the agent and returns a 
     list of all nearby targets.

    :param player: player object (agent.Agent)
    :param balloons: list of balloons (list[balloon.Balloon])
    :agents: list of agents (list[agent.Agent])
    :param fov_radius: field of view radius (int)
    :return: list of balloons (list[balloon.Balloon])
    """
    fov = []
    for b in balloons:
        if(np.linalg.norm(b.coords - player.pos_virtual) < fov_radius):
            fov.append([b.coords[0], b.coords[1], 1])
    # for a in agents:
    #     if(np.linalg.norm(a.pos_virtual - player.pos_virtual) < fov_radius) \
    #         and a != player:
    #         fov.append([a.pos_virtual[0], a.pos_virtual[1], 1])
    return fov