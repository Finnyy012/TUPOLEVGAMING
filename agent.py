import math
import string
import sys
import time
import numpy as np

import aircraft
import settings
import bullet 

class Agent(aircraft.Aircraft):
    """
    Agent class.

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

    + radius_fov: (int) radius of field of view
    + perception_front_dims: (tuple[float, float]) dimensions of
     'danger-zone'
    + nearest_target_pos_abs: (np.ndarray) distance to nearest
     target, relative to origin
    + timestart: (float) UNIX time at initialisation, for debug
    + action: (str) current action, for debug
    + circle_coords: (np.ndarray) coordinates of circle for
     `diff_overlap_circle`
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
        plane_size: tuple[int, int] = (24, 13),
        evade_zone: tuple[int, int] = np.array((150, 30))
    ) -> None:
        """
        Initaliser for Agent

        :param window_dimensions: dimensions of pygame window
         (tuple[float, float])
        :param sprite: filepath to sprite (str)
        :param sprite: filepath to top view sprite (str)
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
        :param evade_zone: evade things in this area (tuple[int, int])
        """

        super().__init__(
            window_dimensions,
            sprite,
            sprite_top,
            mass,
            engine_force,
            agility,
            c_drag,
            c_lift,
            AoA_crit_low,
            AoA_crit_high,
            cl0,
            cd_min,
            init_throttle,
            init_pitch,
            init_v,
            init_pos,
            plane_size
        )

        # dangerzone
        self.radius_fov = 150
        self.perception_front_dims = evade_zone
        self.nearest_target_pos_abs = []

        # debug
        self.testv  = [0,0]
        self.testv2 = [0,0]
        self.testv3 = [0,0]
        self.timestart = time.time()
        self.action = 'none'
        # internal state
        self.bullets = []
        self.history_scale = 10
        self.history = np.zeros((
            2,
            int(window_dimensions[0]/self.history_scale),
            int(window_dimensions[1]/self.history_scale)
        ))

        # np wizardry
        self.r_fov = 150
        self.do_x, self.do_y = np.indices((
            int(window_dimensions[0]/self.history_scale),
            int(window_dimensions[1]/self.history_scale)
        ))

        circle_coords = np.array([
            [9, 0],
            [9, 1],
            [9, 2],
            [8, 3],
            [8, 4],
            [7, 5],
            [7, 6],
            [6, 7],
            [5, 7],
            [4, 8],
            [3, 8],
            [2, 9],
            [1, 9],
            [0, 9]
        ])
        c_temp = circle_coords.copy()
        c_temp[:, 0] = -c_temp[:, 0]
        circle_coords = np.concatenate([c_temp, circle_coords], 0)
        self.circle_coords = np.concatenate([-circle_coords, circle_coords], 0)

    def tick(self, dt: float, fov: np.ndarray) -> None:
        """
        'tick' function; updates internal state

        :param dt: (float) time since last frame in s
        :param fov: (np.ndarray) targets within fov (passed from main)
        :return: None
        """
        super().tick(dt, fov)
        self.update_history(fov)
        self.explore(dt, fov)

    def explore(self, dt, fov):
        """
        'explore' function; steers the aircraft such that
        (in order of priority):
         - targets are avoided
         - ground/ceiling are avoided
         - as much area as possible is discovered

        :param dt: (float) time since last frame in s
        :param fov: (np.ndarray) targets within fov (passed from main)
        :return: None
        """
        d_nearest_target = sys.maxsize
        rotation_matrix = np.array([[
            math.cos((-self.pitch) * math.pi / 180),
            -math.sin((-self.pitch) * math.pi / 180)
        ], [
            math.sin((-self.pitch) * math.pi / 180),
            math.cos((-self.pitch) * math.pi / 180)
        ]])
        evade_direction = 0

        for target in fov:
            d = np.matmul((target[:2]-self.rot_rect.center), rotation_matrix)
            self.nearest_target_pos_abs = d
            if (
                0 < d[0] < self.perception_front_dims[0]
            ) and (
                d[0] < d_nearest_target
            ):
                if 0 < d[1] < self.perception_front_dims[1]:
                    if (
                        target[1] > (
                            settings.GROUND["COLL_ELEVATION"] - (
                                2 * self.perception_front_dims[1]
                            )
                        )
                    ) and (
                        self.v_uv[0] < 0
                    ):
                        evade_direction = -1
                    elif (
                        target[1] < (2 * self.perception_front_dims[1])
                    ) and (
                        self.v_uv[0] > 0
                    ):
                        evade_direction = -1
                    else:
                        evade_direction = 1
                elif 0 < -d[1] < self.perception_front_dims[1]:
                    if (
                        target[1] > (
                            settings.GROUND["COLL_ELEVATION"] - (
                                2 * self.perception_front_dims[1]
                            )
                        )
                    ) and (
                        self.v_uv[0] > 0
                    ):
                        evade_direction = 1
                    elif (
                        target[1] < (2 * self.perception_front_dims[1])
                    ) and (
                        self.v_uv[0] < 0
                    ):
                        evade_direction = 1
                    else:
                        evade_direction = -1

        if evade_direction != 0:
            self.adjust_pitch(dt*evade_direction)
        else:
            safe_d = 10
            safe_slope = 0.2
            flip_cone_slope = 0.9
            if self.orientation == 1 and (-flip_cone_slope > self.v_uv[0]):
                self.flip()
            elif self.orientation==-1 and (flip_cone_slope < self.v_uv[0]):
                self.flip()
            if (
                (
                    self.pos_virtual[1] + self.v_uv[1] * self.radius_fov
                ) > (
                    settings.GROUND["COLL_ELEVATION"] - safe_d
                )
            ) and (
                self.v_uv[1] >= -safe_slope
            ):
                self.action = 'floor'
                if self.v_uv[0] > 0:
                    self.adjust_pitch(dt)
                else:
                    self.adjust_pitch(-dt)
            elif (
                self.pos_virtual[1] + self.v_uv[1] * self.radius_fov < safe_d
            ) and (
                self.v_uv[1] <= safe_slope
            ):
                self.action = 'ceiling'
                if self.v_uv[0] > 0:
                    self.adjust_pitch(-dt)
                else:
                    self.adjust_pitch(dt)
            else:
                self.action = 'explore'
                best = 0
                best_circle = []
                for center in self.circle_coords:
                    n_new = np.sum(self.diff_overlap_circle(center))
                    if n_new == best:
                        best = n_new
                        best_circle.append(center)
                    elif n_new > best:
                        best = n_new
                        best_circle = [center]
                if len(best_circle) == 1:
                    best_circle = best_circle[0]
                elif best == 0:
                    best_circle = np.average(
                        np.where(
                            self.history[0][
                                :, :int(
                                    settings.GROUND["COLL_ELEVATION"] /
                                    self.history_scale
                                )
                            ] == 0
                        ), axis=1
                    )*self.history_scale
                    best_circle -= self.pos_virtual
                    self.action = 'explore tiebreak'
                    best_circle[1] = -best_circle[1]
                else:
                    best_circle = best_circle[0]
                    pass  # TODO: gelijk aantal vakkies in de buut

                diff_head = (
                    math.atan2(best_circle[0], best_circle[1]) -
                    math.atan2(self.v[0], self.v[1])
                ) * 180 / math.pi

                if diff_head > 180:
                    diff_head -= 360
                elif diff_head < -180:
                    diff_head += 360
                if diff_head < 0:
                    self.adjust_pitch(dt)
                elif diff_head > 0:
                    self.adjust_pitch(-dt)

    def update_history(self, fov: np.ndarray) -> None:
        """
        Updates the history matrix with:
         - history of position/pitch
         - history of fov
         - history of targets

        :param fov: (np.ndarray) np array with targets in fov,
         passed from main
        :return: None
        """
        self.history[0][
            int((self.rot_rect.centerx-1)/self.history_scale)
        ][
            int((self.rot_rect.centery-1)/self.history_scale)
        ] = time.time()-self.timestart + 10  # self.pitch
        for x in fov:
            self.history[1][
                int(x[0]/self.history_scale)
            ][
                int(x[1]/self.history_scale)
            ] = x[2]
        self.history[0] += self.diff_overlap_circle()

    def diff_overlap_circle(
        self,
        offset: tuple[int, int] = (0, 0)
    ) -> np.ndarray:
        """
        Returns the logical and of the circle with radius `r_fov` and
        centre `offset`, and the unexplored area. Effectively returns
        the area that would be discovered if the agent were to move to
        `offset`

        :param offset: (tuple[int, int]) centre of circle
        :return: (np.ndarray) new area
        """
        d_agent_x = (
            self.do_x -
            self.pos_virtual[0]/self.history_scale +
            offset[0]/self.history_scale
        )
        d_agent_y = (
            self.do_y -
            self.pos_virtual[1]/self.history_scale +
            offset[1]/self.history_scale
        )
        in_fov = (
            np.sqrt(
                d_agent_x ** 2 + d_agent_y ** 2
            ) < (
                self.r_fov/self.history_scale
            )
        )
        return np.logical_and(
            in_fov, ~(self.history[0].astype(bool))
        ).astype(int)

    def shoot(self):
        self.bullets.append(
            bullet.Bullet(
                self.pos_virtual,
                self.pitch,
                settings.GROUND["COLL_ELEVATION"],
                settings.BULLET["SPRITE"]
            )
        )
    
