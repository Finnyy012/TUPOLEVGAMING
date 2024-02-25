import math
import string
import pygame
import numpy as np


class Aircraft:
    """
    Aircraft class.

    @Attributes:
    - engine_power (float): Engine power of aircraft, in Neutons (N).
    - agility (float): Degree to which the pitch can change, 
     in degrees per delta.
    - mass (float): Mass of aircaft, in Killograms (Kg).
    - c_drag (float): ?
    - c_lift (float): ?
    - throttle (float): Throttle of aircraft.
    - pitch (float): Pitch of aircraft.
    - v (tuple[float, float]): Velocity of aircraft.
    - pos (tuple[int, int]): Position of aircraft (x,y).
    - sprite (pygame.Surface): Container for aircraft sprite.
    - rot_sprite (pygame.Surface): Rotation of sprite.
    - rot_rect (pygame.Rect): Rotation rectangle of sprite.

    The six attributes below are stored in `np.ndarray`s 
     and contain exactly 2 values. 
    The first is the force on the x-axis 
     and the second the force on the y-axis.
    - pitch_uv (np.ndarray): ?
    - v_uv (np.ndarray): ?
    - f_gravity (np.ndarray): Force of gravity.
    - f_engine (np.ndarray): Force of engine.
    - f_drag (np.ndarray): Force of drag.
    - f_lift (np.ndarray): Force of lift.

    @Methods:
    - __init__(
        mass: float,
        engine_power: float,
        agility: float,  
        c_drag: float,
        c_lift: float,
        sprite: string,
        init_throttle: float,
        init_pitch: float,
        init_v: tuple[float, float],
        init_pos: tuple[int, int]
      )-> None
      Initializer for Aircraft.
    - tick(dt: float)-> None
      Update internal state of aircraft over given time interval.
    - adjust_pitch(dt: float)-> None
      Update pitch of aircraft over given time interval.
    """

    def __init__(
        self,
        mass: float,
        engine_power: float,
        agility: float,  
        c_drag: float,
        c_lift: float,
        sprite: string,
        init_throttle: float,
        init_pitch: float,
        init_v: tuple[float, float],
        init_pos: tuple[int, int]
    )-> None:
        """
        Initalizer for Aircraft

        @Parameters:
        - mass (float): Mass of aircaft, in Killograms (Kg).
        - engine_power (float): Engine power of aircraft, 
         in Neutons (N).
        - agility (float): Degree to which the pitch can change, 
         in degrees per delta.
        - c_drag (float): ?
        - c_lift (float): ?
        - sprite (string): Filepath to sprite used for visualisation.
        - init_throttle (float): Initial throttle of aircraft at spawn.
        - init_pitch (float): Initial pitch of aircraft at spawn.
        - init_v (tuple[float, float]): 
         Initial velocity vector of aircraft at spawn.
        - init_pos: (tuple[int int]): 
         Initial spawning location of aircraft (x, y).
        """

        # Constants
        self.engine_power = engine_power
        self.agility = agility  # TODO 1: moment afhankelijk van AoA en v
        self.mass = mass
        self.c_drag = c_drag  # TODO 2: Cd afhankelijk van AoA
        self.c_lift = c_lift  # TODO 3: Cl afhankelijk van AoA

        # Variables
        self.throttle = init_throttle
        self.pitch = init_pitch
        self.v = np.array(init_v)
        self.pos = np.array(init_pos)

        # Dependant variables (Numpy containers)
        self.pitch_uv = np.array([0.0, 0.0])
        self.v_uv = np.array([0.0, 0.0])
        self.f_gravity = np.array([0.0, 9.81*mass])
        self.f_engine = np.array([0.0, 0.0])
        self.f_drag = np.array([0.0, 0.0])
        self.f_lift = np.array([0.0, 0.0])

        # Sprite info
        self.sprite = pygame.image.load(sprite)
        self.rot_sprite = pygame.transform.scale_by(self.sprite, 0.05)
        self.sprite = pygame.transform.scale_by(self.sprite, 0.05)
        self.rot_rect = self.sprite.get_rect(center=init_pos)

    def tick(self, dt: float)-> None:
        """
        Update internal state of aircraft over given time interval.
        
        @Parameters:
        - dt (float): 
         Delta time over which changes need to be calculated.
        """
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self.pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self.pitch)
        
        # f = m * a
        self.f_engine = self.throttle * 0.1 * self.engine_power * \
            self.pitch_uv / self.mass   

        # Schalar projection
        v_head = np.dot(self.v, self.pitch_uv) / np.linalg.norm(self.pitch_uv)  
        # Cl * r * (v^2)/2 * A -> C * (v^2)
        norm_lift = self.c_lift * np.linalg.norm(v_head)**2
        self.f_lift[0] = \
            norm_lift * np.cos(-math.pi/180 * ((self.pitch + 90) % 360))
        self.f_lift[1] = \
            norm_lift * np.sin(-math.pi/180 * ((self.pitch + 90) % 360))

        ########################### NOTE: dit is nattevingerwerk; comment weg als het niet werkt
        if np.linalg.norm(self.v) != 0:
            self.v_uv = self.v / np.linalg.norm(self.v)
        AoA_rad = np.arccos(np.dot(self.v_uv, self.pitch_uv))
        AoA_multiplier = 10
        ###########################

        norm_drag = self.c_drag * np.linalg.norm(self.v)**2
        if np.linalg.norm(self.v) != 0:
            self.f_drag = -norm_drag * self.v / np.linalg.norm(self.v) * \
                (1+AoA_rad**2*AoA_multiplier)

        f_res = self.f_engine + self.f_gravity + self.f_drag + self.f_lift
        self.v += dt * f_res
        self.pos += self.v * dt
        self.rot_rect.centerx = self.pos[0]
        self.rot_rect.centery = self.pos[1]

    def adjust_pitch(self, dt: float):
        """
        Update pitch of aircraft over given time interval.
        
        @Parameters:
        - dt (float): Delta time over which changes need to be calculated.
        """
        self.pitch = (self.pitch + self.agility * dt) % 360
        self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
        self.rot_rect = self.rot_sprite.get_rect(
            center=self.sprite.get_rect(center=self.rot_rect.center).center
        )


# sources:
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/drageq.html
