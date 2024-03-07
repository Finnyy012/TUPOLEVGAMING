import math
import string
import pygame
import numpy as np


class Aircraft:
    """
    Aircraft class.

    @Attributes:
    - window_dimensions (tuple[float, float]): Dimensions of window.
    - engine_power (float): Engine power of aircraft, in Neutons (N).
    - agility (float): Degree to which the pitch can change, 
     in degrees per delta.
    - mass (float): Mass of aircaft, in Killograms (Kg).
    - c_drag (float): 
     'constants' when calculating drag, 
      such as air density and wing area
    - c_lift (float): 
     'constants' when calculating lift, 
      such as air density and wing area
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
    - pitch_uv (np.ndarray): unitvector in the direction of pitch
    - v_uv (np.ndarray): unitvecor in the direction of the velocity vector
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
        window_dimensions: tuple[float, float],
        sprite: string,
        mass: float = 12,
        engine_force: float = 10,
        agility: float = 100,
        c_drag: float = 0.002,
        c_lift: float = 0.01,
        AoA_crit_low: tuple[float, float] = (-15.0, -0.95),
        AoA_crit_high: tuple[float, float] = (19.0, 1.4),
        cl0: float = 0.16,
        cd_min: float = 0.25,
        init_throttle: float = 0,
        init_pitch: float = 0,
        init_v: tuple[float, float] = (0, 0),
        init_pos: tuple[int, int] = (0, 0)
    )-> None:
        """
        Initaliser for Aircraft

        @Parameters:
        - window_dimensions (tuple[float, float]): Dimensions of window.
        - sprite (string): Filepath to sprite used for visualisation.
        - mass (float): Mass of aircraft in Kilogram (Kg).
        - engine_force (float): constant forward force in Newton (N).
        - agility (float): 
         constant torque applied 
         when pressing A or D in degrees per frame.
        - c_drag (float): 
         'constants' when calculating drag, 
          such as air density and wing area
        - c_lift (float): 
         'constants' when calculating lift, 
          such as air density and wing area
        - AoA_crit_low (tuple[float, float]): 
         negative critical angle of attack in degrees and
         its accompanying lift coefficient
        - AoA_crit_high (tuple[float, float]): 
         positive critical angle of attack in degrees and
         its accompanying lift coefficient
        - cl0 (float): lift coefficient at AoA == 0
        - cd_min (float): 
         apex of drag curve; drag coefficient at AoA == 0
        - init_throttle (float): Throttle of aircraft at spawn.
        - init_pitch (float): Pitch of aircraft at spawn.
        - init_v (tuple[float, float]): 
         velocity vector of aircraft at spawn.
        - init_pos: (tuple[int int]): 
         spawning location of aircraft (x, y).
        """
        self.window_dimensions = window_dimensions

        # Constants
        self.mass = mass
        self.engine_force = engine_force
        self.agility = agility
        self.const_drag = c_drag
        self.const_lift = c_lift
        self.AoA_crit_low = AoA_crit_low
        self.AoA_crit_high = AoA_crit_high
        self.cl0 = cl0
        self.cd_min = cd_min

        # initialisable Variables
        self.throttle = init_throttle
        self.pitch = init_pitch
        self.v = np.array(init_v)
        self.pos = np.array(init_pos)

        # Dependant variables (oa Numpy containers)
        self.AoA_deg = 0
        self.pitch_uv = np.array([0.0, 0.0])
        self.v_uv = np.array([0.0, 0.0])
        self.f_gravity = np.array([0.0, 9.81*mass])
        self.f_engine = np.array([0.0, 0.0])
        self.f_drag = np.array([0.0, 0.0])
        self.f_lift = np.array([0.0, 0.0])

        # Sprite info
        self.sprite = pygame.image.load(sprite)
        # self.rot_sprite = pygame.transform.scale_by(self.sprite, 0.05)
        self.rot_sprite = pygame.transform.scale(self.sprite, (24,13))  # TODO: nog even naar groottes kijken
        # self.sprite = pygame.transform.scale_by(self.sprite, 0.05
        self.sprite = pygame.transform.scale(self.sprite, (24,13))
        self.rot_rect = self.sprite.get_rect(center=init_pos)

    def tick(self, dt: float)-> None:
        """
        Update internal state of aircraft over given time interval.
        
        @Parameters:
        - dt (float): 
         Delta time over which changes need to be calculated.
        """
        # pitch unit vector
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self.pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self.pitch)

        # velocity unit vector
        if np.linalg.norm(self.v) != 0:
            self.v_uv = self.v / np.linalg.norm(self.v)

        # angle of attack
        self.AoA_deg = (math.atan2(self.pitch_uv[0], self.pitch_uv[1]) - math.atan2(self.v[0], self.v[1]))*180/math.pi
        if self.AoA_deg > 180:
            self.AoA_deg -= 360
        elif self.AoA_deg < -180:
            self.AoA_deg += 360

        # engine force vector
        self.f_engine = self.throttle * 0.1 * self.engine_force * self.pitch_uv

        # lift force vector
        coef_lift = self.lift_curve(self.AoA_deg)
        norm_lift = self.const_lift * coef_lift * np.linalg.norm(self.v)**2
        self.f_lift[0] = norm_lift * self.v_uv[1]
        self.f_lift[1] = norm_lift * -self.v_uv[0]

        # drag force vector
        coef_drag = (self.AoA_deg / (math.sqrt(40)))**2 + self.cd_min
        norm_drag = self.const_drag * coef_drag * np.linalg.norm(self.v) ** 2
        self.f_drag = -norm_drag * self.v_uv

        # resulting force vector, update velocity & position
        f_res = self.f_engine + self.f_gravity + self.f_drag + self.f_lift
        self.v += dt * f_res / self.mass 
        self.pos += self.v * dt
        self.rot_rect.centerx = (self.pos[0]*4) % self.window_dimensions[0]
        self.rot_rect.centery = (self.pos[1]*4) % self.window_dimensions[1]

        # induced torque (close enough)
        if self.AoA_deg < self.AoA_crit_low[0]:
            self.adjust_pitch(norm_drag*0.0001*dt)
        if self.AoA_deg > self.AoA_crit_high[0]:
            self.adjust_pitch(-norm_drag*0.0001*dt)

    def adjust_pitch(self, dt: float):
        """
        Update pitch of aircraft over given time interval.
        
        @Parameters:
        - dt (float): 
         Delta time over which changes need to be calculated.
        """
        self.pitch = (self.pitch + self.agility * dt) % 360
        self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
        self.rot_rect = self.rot_sprite.get_rect(
            center=self.sprite.get_rect(center=self.rot_rect.center).center
        )

    def lift_curve(self, AoA: float):
        '''
        Lift curve function based on critical angles and cl0

        :param AoA: angle of attack
        :return: lift coefficient at AoA
        '''
        if AoA < self.AoA_crit_low[0]-1:
            return 0.0
        elif self.AoA_crit_low[0]-1 <= AoA < self.AoA_crit_low[0]:
            return self.AoA_crit_low[1] * abs(self.AoA_crit_low[0]-1 - AoA)
        elif self.AoA_crit_low[0] <= AoA < 0.0:
            b = self.cl0 - self.AoA_crit_low[1]
            c = AoA / self.AoA_crit_low[0]
            return self.cl0 - b * c
        elif 0.0 <= AoA < self.AoA_crit_high[0]:
            b = self.AoA_crit_high[1] - self.cl0
            c = AoA / self.AoA_crit_high[0]
            return self.cl0 + b * c
        elif self.AoA_crit_high[0] <= AoA < self.AoA_crit_high[0]+1:
            return self.AoA_crit_high[1] * abs(self.AoA_crit_high[0]-1 - AoA)
        else:
            return 0



# sources:
# https://github.com/gszabi99/War-Thunder-Datamine/tree/master/aces.vromfs.bin_u/gamedata/flightmodels
# https://en.wikipedia.org/wiki/Drag_curve
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/drageq.html
# https://www.aerodynamics4students.com/aircraft-performance/drag-and-drag-coefficient.php

