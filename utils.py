import settings
import pygame
import numpy as np

import agent
import aircraft
import bullet as bullet
import target


def hit_detection_and_move_projectiles(
        targets: target.Target,
        agents: list[agent.Agent],
        current_agent: agent.Agent,
        dt: float
    ) -> None:
    """
    This function checks if a bullet hits a target.
    
    :param targets: list of target (list[target.Target])
    :param agents: list of agents (list[agent.Agent])
    :param current_agent: current agent (agent.Agent)
    :param dt: time step (float)
    :return: None
    """


    for projectile in current_agent.bullets:
        if projectile.move_bullet(dt):
            current_agent.bullets.remove(projectile)
            continue
        for agent in agents:
            if np.linalg.norm(np.array(agent.rot_rect.center) - \
               np.array(projectile.rect.center)) <= 5 and \
               agent != current_agent:
                current_agent.bullets.remove(projectile)
                agents.remove(agent)
                continue

        for orb in targets:
            if projectile.rect.colliderect(orb.rect):
                current_agent.bullets.remove(projectile)
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
                
                
def hit_collision_agents(
        targets: list[target.Target],
        player: aircraft.Aircraft
    ) -> bool:
    """
    This function checks if the player hits a target. If a player
     hits a target, the function returns True.

    :param targets: list of target (list[target.Target])
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
        targets: list[target.Target],
        ground_height: int
    ) -> list[target.Target]:
    """
    This function generates new targets if the number of targets is 
     less than the defined amount in settings.py. Ground height is used
     to spawn targets above the ground.
    
    :param targets: list of target (list[target.Target])
    :param ground_height: height of the ground (int)
    :return: list of target (list[target.Target])
    """
    if len(targets) < settings.TARGET["TARGET_COUNT"]:
        new_targets = target.load_single_type_targets(
            ground_height,
            settings.TARGET["TARGET_COUNT"] - len(targets)
        )
        new_targets.extend(targets)
        return new_targets
    else:
        return targets


def display_targets(
        targets: list[target.Target],
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the targets on the screen.
    
    :param targets: list of targets (list[Target])
    :param screen: screen (pygame.Surface)
    :return: None
    """
    for target in targets:
        screen.blit(
            target.sprite, target.coords
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
        current_agent: agent.Agent, 
        targets: list[target.Target], 
        agents : list[agent.Agent],
        fov_radius: int
    ) -> list: 
    """
    This function checks the surrounding of the agent and returns a 
     list of all nearby targets.

    :param player: player object (agent.Agent)
    :param targets: list of targets (list[TARGET.TARGET])
    :agents: list of agents (list[agent.Agent])
    :param fov_radius: field of view radius (int)
    :return: list of targets (list[TARGET.TARGET])
    """
    fov = []
    for target in targets:
        if(
            np.linalg.norm(target.coords - current_agent.pos_virtual) < 
            fov_radius
        ):
            fov.append([target.coords[0], target.coords[1], 1])
        # check if fov_radius circle moves 
        #  out of frame on the right side of the screen
        elif(
            current_agent.pos_virtual[0] + fov_radius > 
            settings.SCREEN_WIDTH
        ):
            # place circle outside of the screen on the left
            if(
                np.linalg.norm(
                    target.coords - (
                        settings.SCREEN_WIDTH - (
                            current_agent.pos_virtual[0] + 
                            fov_radius
                        ), 
                        current_agent.pos_virtual[1]
                    )
                ) < 
                fov_radius
            ):
                fov.append([target.coords[0], target.coords[1], 1])
        # check if fov_radius circle moves 
        #  out of frame on the left side of the screen
        elif(current_agent.pos_virtual[0] - fov_radius < 0):
            # place circle outside of the screen on the right
            if(
                np.linalg.norm(
                    target.coords - (
                        settings.SCREEN_WIDTH + 
                        current_agent.pos_virtual[0],
                        current_agent.pos_virtual[1]
                    )
                ) < 
                fov_radius
            ):
                fov.append([target.coords[0], target.coords[1], 1])
    for agent in agents:
        if(np.linalg.norm(agent.pos_virtual - current_agent.pos_virtual) < fov_radius) \
            and agent != current_agent:
            fov.append([agent.pos_virtual[0], agent.pos_virtual[1], 1])
    return fov

