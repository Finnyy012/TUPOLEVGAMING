import pygame


class Ground:
    """
    Ground class

    @Attributes
    - sprite (pygame.surface) optional sprite with contents of ground.
    - elevation (int): Elevation seen from the bottom, in pixels.
    - coll_elevation (int): 
     Elevation from which point the player crashes upon intersection.

    @Methods:
    __init__(
        self, 
        height: int, 
        elevation: int, 
        coll_elevation: int,
        sprite: str=None,
        resolution: tuple[int, int]=None
    )-> None
    """
    def __init__(
            self, 
            height: int, 
            elevation: int, 
            coll_elevation: int,
            sprite: str=None,
            resolution: tuple[int, int]=None
        ) -> None:
        """
        initialiser Ground class

        :param height: height of sprite (int)
        :param elevation: elevation seen from the bottom, in pixels (int)
        :param coll_elevation: elevation from which point the player crashes
        upon intersection; recommended to make this slightly above the floor,
        for realism (int)
        :param sprite: path to sprite (str)
        :param resolution: resolution of game window (tuple[int, int])
        """
        self.sprite = None
        if sprite:
            self.sprite = pygame.transform.scale(
                pygame.image.load(sprite), 
                (resolution[0], height)
            )
        self.elevation = elevation
        self.coll_elevation = coll_elevation
