import settings
import pygame
import numpy as np

import aircraft
import bullet as bullet
import target


def hit_detection_and_move_projectiles(
        projectiles: bullet.Bullet,
        targets: target.Target,
        dt: float
    ) -> None:
    """
    This function checks if a bullet hits a balloon.
    
    :param projectiles: list of bullets (list[bullet.Bullet])
    :param targets: list of balloons (list[balloon.Target])
    :param dt: time step (float)
    :return: None
    """
    for projectile in projectiles:
        if projectile.move_bullet(dt):
            projectiles.remove(projectile)
            continue
        for orb in targets:
            if projectile.rect.colliderect(orb.rect):
                projectiles.remove(projectile)
                targets.remove(orb)
                
                
def hit_collision_player(
        targets: list[target.Target],
        player: aircraft.Aircraft
    ) -> bool:
    """
    This function checks if the player hits a balloon. If a player
     hits a balloon, the function returns True.

    :param targets: list of balloons (list[Target])
    :param player: player object (aircraft.Aircraft)
    :return: bool
    """
    for target in targets:
        if np.linalg.norm(
            np.array(player.rot_rect.center) - target.coords
        ) < 15:
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
    
    :param targets: list of balloons (list[Target])
    :param ground_height: height of the ground (int)
    :return: list of balloons (list[Target])
    """
    if len(targets) < settings.BALLOON["BALLOON_COUNT"]:
        new_targets = target.load_single_type_balloons(
            ground_height,
            settings.BALLOON["BALLOON_COUNT"] - len(targets)
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
    
    :param targets: list of balloons (list[Target])
    :param screen: screen (pygame.Surface)
    :return: None
    """
    for plastic_orb in targets:
        screen.blit(
            plastic_orb.sprite, plastic_orb.coords
        )


def display_projectiles(
        projectiles: list[bullet.Bullet],
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the bullets on the screen.

    @Parameters:
    :param projectiles: list of bullets (list[bullet.Bullet])
    :param screen: screen (pygame.Surface)
    :return: None
    """
    for projectile in projectiles:
        screen.blit(
            pygame.transform.flip(
                projectile.sprite,
                True, 
                False
                ), 
            projectile.coords
        )