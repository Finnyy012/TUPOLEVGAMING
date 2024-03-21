import settings
import random
import pygame
import numpy as np

import aircraft
import bullet
import balloon


def hit_detection_and_move_bullets(
        bullets: bullet.Bullet, 
        targets: balloon.Balloon, 
        dt: float
    ) -> None:
    """
    This function checks if a bullet hits a balloon.
    
    @Parameters:
    - bullets (list): list of bullets
    - targets (list): list of targets
    - dt (float): time step

    @Returns:
    - None
    """
    for bt in bullets:
        if bt.move_bullet(dt):
            bullets.remove(bt)
            continue
        for orb in targets:
            if bt.rect.colliderect(orb.rect):
                bullets.remove(bt)
                targets.remove(orb)
                
                
def hit_collision_player(
        targets: list[balloon.Balloon], 
        player: aircraft.Aircraft
    ) -> bool:
    """
    This function checks if the player hits a balloon.

    @Parameters:
    - targets (list): list of targets
    - player (Player): player object

    @Returns:
    - bool: True if the player hits a balloon, False otherwise
    """
    for balloon in targets:
        if np.linalg.norm(
            np.array(player.rot_rect.center) - balloon.coords
        ) < 15:
            return True
    return False
    
    
def create_balloons(
        targets: list[balloon.Balloon], 
        ground_height: int
    ) -> list[balloon.Balloon]:
    """
    This function generates new targets if the number of targets is 
     less than the defined amount in settings.py. Ground height is used
     to spawn targets above the ground.
    
    @Parameters:
    - targets (list): list of targets
    - ground_height (int): height of the ground

    @Returns:
    - list: list of targets
    """
    if len(targets) < settings.BALLOON["BALLOON_COUNT"]:
        new_targets = balloon.load_single_type_balloons(ground_height)
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

    @Parameters:
    - targets (list): list of targets
    - screen (pygame.Surface): screen

    @Returns:
    - None
    """
    for plastic_orb in targets:
        screen.blit(
            plastic_orb.sprite, plastic_orb.coords
        )


def display_bullets(
        bullets: list[bullet.Bullet], 
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the bullets on the screen.

    @Parameters:
    - bullets (list): list of bullets
    - screen (pygame.Surface): screen

    @Returns:
    - None
    """
    for bt in bullets:
        screen.blit(
            pygame.transform.flip(
                bt.sprite, 
                True, 
                False
                ), 
            bt.coords
        )
