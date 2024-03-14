import pygame
import random

import settings

class Balloon:
    def __init__(self, sprite, ground_height: str=None)-> None:
        """
        Initaliser of the balloon class

        @Parameters:
        - sprite (string): 
         path of the image used for the sprite of the balloon 
         (Default = False)
        
        """
        size = settings.BALLOON["SIZE"]
        self.coords = (
            random.randint(
                size, settings.SCREEN_WIDTH - size
            ), random.randint(
                0, ground_height - size
            )
        )
        self.rect = pygame.Rect(self.coords[0], self.coords[1], size, size)
        pygame.draw.rect(
            surface=pygame.display.get_surface(), 
            color="black", rect=self.rect)
        if sprite:
            self.sprite = pygame.image.load(sprite)        
            self.sprite = pygame.transform.scale(self.sprite, (size, size))    


    def is_hit(self, point)-> bool:
        """
        This function checks if the balloon is hit.
        
        @Parameters:
        - point (tuple): position of the event that needs to be checked
                         (pygame.event.pos) 

        @Returns:
        - bool: True if the point is within the balloon, False otherwise
        """
        return self.rect.collidepoint(point)
