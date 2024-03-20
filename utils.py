import settings
import random
import pygame
import numpy as np

import aircraft
import bullet
import ground
import balloon


def hit_detection_and_move_bullets(
        bullets: bullet.Bullet, 
        balloons: balloon.Balloon, 
        dt: float
    ) -> None:
    """
    This function checks if a bullet hits a balloon.
    
    @Parameters:
    - bullets (list): list of bullets
    - balloons (list): list of balloons
    - dt (float): time step

    @Returns:
    - None
    """
    for bt in bullets:
        if bt.move_bullet(dt):
            bullets.remove(bt)
            continue
        for orb in balloons:
            if bt.rect.colliderect(orb.rect):
                bullets.remove(bt)
                balloons.remove(orb)
                
                
def hit_collision_player(
        balloons: list[balloon.Balloon], 
        player: aircraft.Aircraft
    ) -> bool:
    """
    This function checks if the player hits a balloon.

    @Parameters:
    - balloons (list): list of balloons
    - player (Player): player object

    @Returns:
    - bool: True if the player hits a balloon, False otherwise
    """
    for balloon in balloons:
        if np.linalg.norm(np.array(player.rot_rect.center)-balloon.coords)<15:
            return True
    return False
    
    
def create_balloons(
        balloons: list[balloon.Balloon], 
        ground_height: int
    ) -> list[balloon.Balloon]:
    """
    This function generates new balloons if the number of balloons is 
     less than the defined amount in settings.py. Ground height is used
     to spawn balloons above the ground.
    
    @Parameters:
    - balloons (list): list of balloons
    - ground_height (int): height of the ground

    @Returns:
    - list: list of balloons
    """
    if len(balloons) < settings.BALLOON["BALLOON_COUNT"]:
        new_balloons = [
            balloon.Balloon(
                random.choice(settings.BALLOON["SPRITES"]),
                ground_height
            ) for _ in range (
                settings.BALLOON["BALLOON_COUNT"] - len(balloons)
            )
        ]
        new_balloons.extend(balloons)
        return new_balloons
    else:
        return balloons


def display_balloons(
        balloons: list[balloon.Balloon], 
        screen: pygame.Surface
    ) -> None:
    """
    This function displays the balloons on the screen.

    @Parameters:
    - balloons (list): list of balloons
    - screen (pygame.Surface): screen

    @Returns:
    - None
    """
    for plastic_orb in balloons:
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
            bt.coords)
