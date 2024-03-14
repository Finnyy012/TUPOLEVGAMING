import settings
import balloon
import random
import pygame
import aircraft
import bullet
import ground

def hit_detection_and_move_bullets(
        bullets: bullet.Bullet, 
        balloons: balloon.Balloon, 
        dt: float
    ):
    """
    This function checks if a bullet hits a balloon and if the player 
     hits a balloon.
    
    @Parameters:
    - bullets (list): list of bullets
    - balloons (list): list of balloons
    - player (Player): player object
    - dt (float): time step

    @Returns:
    - bool: False if the player hits a balloon, True otherwise
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
        player : aircraft.Aircraft
    ):
    """
    This function checks if the player hits a balloon.

    @Parameters:
    - balloons (list): list of balloons
    - player (Player): player object

    @Returns:
    - bool: True if the player hits a balloon, False otherwise
    """
    for balloon in balloons:
        if player.rot_rect.colliderect(balloon.rect):
            return True
    return False

def hit_collision_environment(floor: ground.Ground, player: aircraft.Aircraft):
    """
    This function checks if the player hits the ground.

    @Parameters:
    - floor (pygame.Rect): ground
    - player (Player): player object

    @Returns:
    - bool: True if the player hits the ground, False otherwise
    """
    if player.rot_rect.bottom >= floor.coll_elevation:
        return True
    return False
    
    
def create_balloons(balloons: list[balloon.Balloon], ground_height: int):
    """
    This function generates new balloons if the number of balloons is 
     less than the defined amount in settings.py.
    
    @Parameters:
    - balloons (list): list of balloons

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
    ):
    """
    This function displays the balloons on the screen.

    @Parameters:
    - balloons (list): list of balloons
    - screen (pygame.Surface): screen
    """
    for plastic_orb in balloons:
        screen.blit(
            plastic_orb.sprite, plastic_orb.coords
        )

def display_bullets(
        bullets: list[bullet.Bullet], 
        screen: pygame.Surface
    ):
    for bt in bullets:
        screen.blit(
            pygame.transform.flip(
                bt.sprite, 
                True, 
                False
                ), 
            bt.coords)