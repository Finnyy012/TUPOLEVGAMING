import pygame


class Ground:
    """
    Ground class

    + sprite: (pygame.Surface) ground sprite
    + elevation: (int) pixels from top of screen to top of ground sprite
    + coll_elevation: (int) pixels from top of screen to in-sprite
       ground
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
        initialiser Ground class

        :param height: height of sprite (int)
        :param elevation: pixels from top of screen to top of
        ground sprite (int)
        :param coll_elevation: pixels from top of screen to in-sprite
        ground (int)
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




