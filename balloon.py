import pygame
import random

class Balloon:
    def __init__(self, sprite: str):
        """
        Initialiser of the balloon class

        @Parameters:
        - sprite (string): 
        path of the image used for the sprite of the balloon
        
        """
        sprite_size = 10
        self.sprite = pygame.image.load(sprite)        
        self.sprite = pygame.transform.scale(self.sprite, (sprite_size, sprite_size))    
        self.coords = (random.randint(0 + sprite_size ,1280 - sprite_size), random.randint(0 + sprite_size, 720 - sprite_size))


    
    
