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
        )-> None:
        """
        Initialize Ground class.

        @Parameters:
        - height (int): Height of sprite
        - elevation (int): Elevation seen from the bottom, in pixels.
        - coll_elevation (int): 
         Elevation from which point the player crashes upon intersection 
         Recommended to make this slightly above the floor, for realism.
        - sprite (str): Path to sprite. (Default = None)
        - resolution (tuple[int, int]): 
         Resolution of sprite. (Default = None)
        """
        self.sprite = None
        if sprite:
            self.sprite = pygame.transform.scale(
                pygame.image.load(sprite), 
                (resolution[0], height)
            )
        self.elevation = elevation
        self.coll_elevation = coll_elevation




