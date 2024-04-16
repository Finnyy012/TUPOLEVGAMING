import pygame
import math

import settings


class Bullet:
    """
    Bullet class

    + sprite: (pygame.surface) optional sprite with contents of bullet
    + size: (int) bullet 2r
    + current_time: (float) accumulator for dt 
    + pitch: (float) pitch of bullet
    + speed: (float) bullet speed (m/s)
    + ground_height: (int) ground_height (pixels)
    + coords: (Tuple[int, int]) location (x, y) (pixels)
    + rect: (Tuple[int, int]) balloon rect
    """
    def __init__(
            self,
            coords: tuple[int, int],
            pitch: float,
            ground_height: int,
            sprite: str=None,
    ) -> None:
        """
        Initaliser of the bullet class

        :param coords: initial position of the bullet (tuple[int, int])
        :param pitch: angle of the bullet (float)
        :param ground_height: height of the ground (int)
        :param sprite: path of the image used for the sprite of the 
         bullet
        :return: None
        """
        self.size = settings.BULLET["SIZE"]
        self.current_time = 0
        self.pitch = pitch
        self.speed = settings.BULLET["SPEED"]
        self.ground_height = ground_height

        self.coords = (
            coords[0],
            coords[1]
        )
        self.rect = pygame.Rect(
            self.coords[0],
            self.coords[1],
            self.size,
            self.size
        )

        if sprite:
            self.sprite = pygame.image.load(sprite)
            self.sprite = pygame.transform.scale(
                self.sprite,
                (self.size, self.size)
            )

    def move_bullet(self, dt: float) -> bool:
        """
        This function calculates the new position of the bullet based on 
        the pitch of the plane. If the bullet has been alive for too
        long, it destroys itself. If the bullet hits the ground, it
        is also destroyed. The function returns True if the bullet
        needs to be destroyed.

        :param dt: time step (float)
        :return: bool
        """
        self.current_time += dt

        # Calculate the new position of the bullet
        dx = self.speed * math.cos(math.radians(-self.pitch))
        dy = self.speed * math.sin(math.radians(-self.pitch))

        self.coords = (self.coords[0] + dx, self.coords[1] + dy)
        self.rect = pygame.Rect(
            self.coords[0],
            self.coords[1],
            self.size,
            self.size
        )

        # Check if the bullet needs to wrap around the screen
        if self.coords[0] < 0:
            self.coords = (settings.SCREEN_WIDTH, self.coords[1])
        elif self.coords[0] > settings.SCREEN_WIDTH:
            self.coords = (0, self.coords[1])

        # Check if the bullet needs to be destroyed
        if self.current_time >= settings.BULLET["LIFETIME"]:
            return True

        if self.coords[1] >= self.ground_height:
            return True
        return False
