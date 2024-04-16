import numpy as np
import pygame
import random

import settings


class Target:
    """
    Target class

    + coords: (Tuple[int, int]) coördinaten
    + rect: (pygame.rect) rect
    + sprite: (pygame.surface) sprite
    """
    def __init__(self, ground_height: int, sprite:str=None) -> None:
        """
        Initaliser of the Target class

        :param ground_height: height of the ground (int)
        :param sprite: path of the image used for the sprite of the (str)
         target (Default = False)
        """
        size = settings.TARGET["SIZE"]
        self.coords = np.array((
            random.randint(
                size, settings.SCREEN_WIDTH - size
            ), random.randint(
                10, ground_height - size
            )
        ))
        self.rect = pygame.Rect(self.coords[0], self.coords[1], size, size)
        self.rect.center = self.coords + (np.array([size, size]) / 2)


        if settings.USE_GUI:
            pygame.draw.rect(
                surface=pygame.display.get_surface(),
                color="black",
                rect=self.rect
            )
            self.sprite = pygame.image.load(sprite)        
            self.sprite = pygame.transform.scale(self.sprite, (size, size))


def load_single_type_targets(
        ground_height: int, target_count: int
) -> list[Target]:
    """
    This function loads a list of target with the same sprite.
    
    :param ground_height: height of the ground (int)
    :param target_count: number of target to be loaded (int)
    :return: list of target (list[Target])
    """
    return [
        Target(
            ground_height,
            settings.TARGET["SPRITE"]
        ) for _ in range(
            target_count
        )
    ]


def load_multiple_types_targets() -> list[Target]:
    """
    This function loads a list of target with different sprites.

    :return: list of target (list[Target])
    """
    # @NOTE:
    # This function can be expanded further once multiple
    #  types of TARGETs are implemented.
    return [
        Target(
            random.choice(
                settings.TARGET["SPRITES"]
            )
        ) for _ in range(
            settings.TARGET["TARGET_COUNT"]
        )
    ]
