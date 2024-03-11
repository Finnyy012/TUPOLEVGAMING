import pygame
import random
from typing import List

import settings
class Balloon:
    def __init__(self, sprite: str) -> None:
        """
        Initaliser of the balloon class

        @Parameters:
        - sprite (string): 
        path of the image used for the sprite of the balloon
        
        """
        size = settings.BALLOON["SIZE"]
        self.coords = (
            random.randint(
                0 + size, 1280 - size
            ), random.randint(
                0 + size, 720 - size
            )
        )
        self.rect = pygame.Rect(self.coords[0], self.coords[1], size, size)

        if sprite:
            self.sprite = pygame.image.load(sprite)        
            self.sprite = pygame.transform.scale(self.sprite, (size, size))    


    def is_hit(self, point) -> bool:
        """
        This function checks if the balloon is hit.
        
        @Parameters:
        - point (tuple): position of the event that needs to be checked
                         (pygame.event.pos) 

        @Returns:
        - bool: True if the point is within the balloon, False otherwise
        """
        return self.rect.collidepoint(point)


def load_single_type_balloons() -> List[Balloon]:
    """
    This function loads a list of balloons with the same sprite.

    @Returns:
    - list: list of balloons
    """
    return [
        Balloon(
            settings.BALLOON["SPRITE"]
        ) for _ in range(
            settings.BALLOON["BALLOON_COUNT"]
        )
    ]


def load_multiple_types_balloons() -> List[Balloon]:
    """
    This function loads a list of balloons with different sprites.

    @Returns:
    - list: list of balloons
    """
    #@NOTE:
    #This function can be expanded further once multiple 
    # types of balloons are implemented.
    return [
        Balloon(
            random.choice(
                settings.BALLOON["SPRITES"]
            )
        ) for _ in range(
            settings.BALLOON["BALLOON_COUNT"]
        )
    ]
