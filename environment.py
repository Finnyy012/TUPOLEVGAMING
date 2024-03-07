import pygame


class Environment:
    def __init__(self, sprite: str, resolution: tuple[int, int], height: int, elevation: int, coll_elevation: int):
        self.sprite = pygame.transform.scale(pygame.image.load(sprite), (resolution[0], height))
        self.elevation = elevation
        self.coll_elevation = coll_elevation




