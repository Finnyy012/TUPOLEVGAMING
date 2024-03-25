import numpy as np
import pygame
import random

import settings


class Balloon:
    def __init__(self, ground_height: int, sprite:str=None) -> None:
        """
        Initaliser of the balloon class

        :param ground_height: height of the ground (int)
        :param sprite: path of the image used for the sprite of the 
         balloon (Default = False)
        """
        size = settings.BALLOON["SIZE"]
        self.coords = np.array((
            random.randint(
                size, settings.SCREEN_WIDTH - size
            ), random.randint(
                0, ground_height - size
            )
        ))
        self.rect = pygame.Rect(self.coords[0], self.coords[1], size, size)
        self.rect.center = self.coords

        pygame.draw.rect(
            surface=pygame.display.get_surface(),
            color="black",
            rect=self.rect
        )

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


def load_single_type_balloons(ground_height: int, target_count: int) -> list[Balloon]:
    """
    This function loads a list of balloons with the same sprite.
    
    :param ground_height: height of the ground (int)
    :param target_count: number of balloons to be loaded (int)
    :return: list of balloons (list(list[Balloon]))
    """
    return [
        Balloon(
            ground_height,
            settings.BALLOON["SPRITE"]
        ) for _ in range(
            target_count
        )
    ]


def load_multiple_types_balloons() -> list[Balloon]:
    """
    This function loads a list of balloons with different sprites.

    @Returns:
    - list (list[Balloon]): list of balloons
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
