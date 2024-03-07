import pygame
import random
import settings

class Balloon:
    def __init__(self, sprite: str):
        """
        initialize of the balloon class

        @Parameters:
        - sprite (string): 
        path of the image used for the sprite of the balloon
        
        """

        size = settings.BALLOON["SIZE"]
        self.coords = (
            random.randint(
                0 + size ,1280 - size
            ), random.randint(
                0 + size, 720 - size
            )
        )
        self.rect = pygame.Rect(self.coords[0], self.coords[1], size, size)

        if sprite:
            self.sprite = pygame.image.load(sprite)        
            self.sprite = pygame.transform.scale(self.sprite, (size, size))    
            # draw_box()

    def is_hit(self, point):
        # pygame.sprite.Sprite.kill(self.sprite)
        return self.rect.collidepoint(point)
            
    
