import pygame
import math
import string
import time
import numpy as np

import settings


class Aircraft:
    """
    Aircraft class.

    + window_dimensions: (tuple[float, float]) dimensions of window
    + mass: (float) mass of aircraft, in kilogram (Kg).
    + engine_force: (float) constant force applied in direction
    of `pitch` in Newtons (N)
    + agility: (float) Degree to which the pitch can change,
    in degrees per delta.
    + c_drag: (float) 'constants' when calculating drag,
    such as air density and wing area
    + c_lift: (float) 'constants' when calculating lift,
    such as air density and wing area
    + AoA_crit_low: (tuple[float, float]) negative critical angle
     of attack in degrees and its corresponding lift coefficient
    + AoA_crit_high: (tuple[float, float]) positive critical angle
     of attack in degrees and its corresponding lift coefficient
    + cl0: (float) lift coefficient at AoA == 0
    + cd_min: (float) apex of drag curve; drag coefficient at AoA == 0
    + plane_size: (tuple[int, int]) dimensions of aircraft
    (length, height) in meter (m)
    + throttle: (float) throttle
    + pitch: (float) pitch in degrees
    + v: (tuple[float, float]) velocity vector
    + pos_real: (tuple[float, float]) aircraft position in m
    + orientation: (int) direction of lift vector
    + flipstart: (float) timer for flip sprite
    + pos_virtual: (tuple[float, float]) aircraft position on screen
    + AoA_deg: (float) angle of attack in deg
    + pitch_uv: (tuple[float, float]) unitvector corresponding to
    `pitch`
    + v_uv: (tuple[float, float]) unitvector corresponding to `v`
    + f_gravity: (tuple[float, float]) gravity force vector
    + f_engine: (tuple[float, float]) engine force vector
    + f_drag: (tuple[float, float]) drag force vector
    + f_lift: (tuple[float, float]) drag force vector
    + use_gui: (bool) true if using GUI
    + sprite: (pygame.Surface) side view sprite
    + rot_sprite: (pygame.Surface) side view sprite, rotated
    + rot_rect: (pygame.Rect) rectangle object for pygame
    + flipsprite: (pygame.Surface) top view sprite
    + spritecontainer: (pygame.Surface) temp container for `flip()`
    """
    def __init__(
        self,
        window_dimensions: tuple[int, int],
        sprite: string = None,
        sprite_top: string = None,
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
        init_pos: tuple[int, int] = (0, 0),
        plane_size: tuple[int, int] = (24, 13)
    ) -> None:
        """
        Initaliser for Aircraft

        :param window_dimensions: dimensions of pygame window
         (tuple[float, float])
        :param sprite: filepath to sprite (str)
        :param sprite_top: filepath to top view sprite (str)
        :param mass: mass of aircraft in Kilogram (Kg) (float)
        :param engine_force: constant force applied in direction of
         heading (pitch) in Newton (N) (float)
        :param agility: constant torque applied when changing pitch in
         degrees per second (°/s) (float)
        :param c_drag: 'constants' used in calculating drag, such as air
         density and wing area (float)
        :param c_lift: 'constants' used in calculating lift, such as air
         density and wing area (float)
        :param AoA_crit_low: negative critical angle of attack in
         degrees and its corresponding lift coefficient
         (tuple[float, float])
        :param AoA_crit_high: positive critical angle of attack in
         degrees and its corresponding lift coefficient
         (tuple[float, float])
        :param cl0: lift coefficient at AoA == 0 (float)
        :param cd_min: apex of drag curve; drag coefficient at AoA == 0
         (float)
        :param init_throttle: throttle at spawn (%) (float)
        :param init_pitch: pitch at spawn (°) (float)
        :param init_v: velocity vector at spawn (tuple[float, float])
        :param init_pos: real spawn location of aircraft
         (tuple[float, float])
        :param plane_size: aircraft sprite dimensions (tuple[int, int])
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

        # Independent Variables
        self.throttle = init_throttle
        self.pitch = init_pitch
        self.v = np.array(init_v)
        self.pos_real = np.array(init_pos)
        self.orientation = 1
        self.flipstart = 0.0

        # Dependent variables (oa Numpy containers)
        self.pos_virtual = (
            self.pos_real *
            settings.PLANE_POS_SCALE %
            self.window_dimensions
        )
        self.AoA_deg = 0
        self.pitch_uv = np.array([0.0, 0.0])
        self.v_uv = np.array([0.0, 0.0])
        self.f_gravity = np.array([0.0, 9.81*mass])
        self.f_engine = np.array([0.0, 0.0])
        self.f_drag = np.array([0.0, 0.0])
        self.f_lift = np.array([0.0, 0.0])

        # Sprite info
        self.use_gui = True
        if sprite == None:
            self.use_gui = False
        if self.use_gui:
            self.sprite = pygame.image.load(sprite)
            self.rot_sprite = pygame.transform.scale(
                self.sprite,
                plane_size
            )
            self.sprite = pygame.transform.scale(
                self.sprite,
                plane_size
            )
            self.rot_rect = self.sprite.get_rect(center=init_pos)

        self.flipsprite = pygame.image.load(sprite_top)
        self.flipsprite = pygame.transform.scale(self.flipsprite, plane_size)
        self.spritecontainer = self.sprite

    def tick(self, dt: float, fov: np.ndarray) -> None:
        """
        Update internal state of aircraft over given time interval.

        :param dt: time since last frame (s) (float)
        :param fov: array containing objects within fov_evade radius (np.ndarray)
        :return: None
        """

        # pitch unit vector
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self.pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self.pitch)

        # velocity unit vector
        if np.linalg.norm(self.v) != 0:
            self.v_uv = self.v / np.linalg.norm(self.v)

        # angle of attack
        self.AoA_deg = (
            math.atan2(self.pitch_uv[0], self.pitch_uv[1]) -
            math.atan2(self.v[0], self.v[1])
        ) * 180 / math.pi
        if self.AoA_deg > 180:
            self.AoA_deg -= 360
        elif self.AoA_deg < -180:
            self.AoA_deg += 360

        # engine force vector
        self.f_engine = self.throttle * 0.1 * self.engine_force * self.pitch_uv

        # lift force vector
        coef_lift = self.lift_curve(self.orientation * self.AoA_deg)
        norm_lift = (
            self.const_lift *
            coef_lift *
            np.linalg.norm(self.v)**2 *
            self.orientation
        )
        self.f_lift[0] = norm_lift * self.v_uv[1]
        self.f_lift[1] = norm_lift * -self.v_uv[0]

        # drag force vector
        coef_drag = (self.AoA_deg / (math.sqrt(40)))**2 + self.cd_min
        norm_drag = self.const_drag * coef_drag * np.linalg.norm(self.v) ** 2
        self.f_drag = -norm_drag * self.v_uv

        # resulting force vector, update velocity & position
        f_res = self.f_engine + self.f_gravity + self.f_drag + self.f_lift
        self.v += dt * f_res / self.mass 
        self.pos_real += self.v * dt
        if self.use_gui:
            self.rot_rect.centerx = self.pos_virtual[0]
            self.rot_rect.centery = self.pos_virtual[1]

        # induced torque (close enough)
        if self.AoA_deg < self.AoA_crit_low[0]:
            self.adjust_pitch(norm_drag*0.0001*dt)
        if self.AoA_deg > self.AoA_crit_high[0]:
            self.adjust_pitch(-norm_drag*0.0001*dt)

        if self.use_gui:
            self.flip_update_sprite()
        self.pos_virtual = (
            self.pos_real *
            settings.PLANE_POS_SCALE %
            self.window_dimensions
        )

    def adjust_pitch(self, dt: float):
        """
        Update pitch of aircraft over given time interval.

        :param dt: Delta time over which changes need to be calculated.
        :return: None
        """
        self.pitch = (self.pitch + self.agility * dt) % 360
        if self.use_gui:
            self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
            self.rot_rect = self.rot_sprite.get_rect(
                center=self.sprite.get_rect(center=self.rot_rect.center).center
            )

    def flip(self):
        """
        Flips orientation of the aircraft and starts timer for
        `flipupdatesprite()`

        :return: None
        """
        if self.flipstart < 0.0000001:
            self.orientation = -self.orientation
        self.flipstart = time.time()

    def flip_update_sprite(self):
        """
        Updates aircraft sprite during orientation flip

        :return: None
        """
        if self.flipstart > 0.0000001:
            # show sprite after .25s
            if .25 < (time.time() - self.flipstart) < .5:
                self.sprite = self.flipsprite
            # reset sprite after .5s
            elif .5 <= (time.time() - self.flipstart):
                if self.orientation == 1:
                    self.sprite = self.spritecontainer
                else:
                    self.sprite = pygame.transform.flip(
                        self.spritecontainer, 
                        0, 
                        1
                    )
                self.flipstart = 0.0

        self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
        self.rot_rect = self.rot_sprite.get_rect(
            center=self.sprite.get_rect(center=self.rot_rect.center).center
        )

    def lift_curve(self, AoA: float):
        """
        Lift curve function based on critical angles and cl0

        :param AoA: angle of attack
        :return: lift coefficient at AoA
        """
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
