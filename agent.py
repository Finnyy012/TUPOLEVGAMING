import math
import string
import time
import numpy as np

import aircraft


class Agent(aircraft.Aircraft):
    def __init__(self,
                 window_dimensions: tuple[int, int],
                 sprite: string = None,
                 mass: float = 12,
                 engine_force: float = 10,
                 agility: float = 100,
                 c_drag: float = 0.002,
                 c_lift: float = 0.01,
                 AoA_crit_low: tuple[float, float] = (-15.0, -0.95),
                 AoA_crit_high: tuple[float, float] = (19.0, 1.4),
                 cl0: float = 0.16, cd_min: float = 0.25,
                 init_throttle: float = 0, init_pitch: float = 0,
                 init_v: tuple[float, float] = (0, 0),
                 init_pos: tuple[int, int] = (0, 0)) -> None:

        super().__init__(window_dimensions,
                         sprite,
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
                         init_pos)
        # dangerzone
        self.perception_front_dims = np.array((150, 30))
        self.nearest_target_pos_abs = []

        # debug
        self.testv  = [0,0]
        self.testv2 = [0,0]
        self.testv3 = [0,0]
        self.timestart = time.time()
        self.action = 'none'

        # internal state
        self.history_scale = 10
        self.history = np.zeros((2,
                                 int(window_dimensions[0]/self.history_scale),
                                 int(window_dimensions[1]/self.history_scale))
                                )

        # np wizardry
        self.r_fov = 150
        self.do_x, self.do_y = np.indices((int(window_dimensions[0]/self.history_scale),
                                           int(window_dimensions[1]/self.history_scale))
                                          )
        circle_coords = np.array([[9, 0],
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
                                  [0, 9]])
        c_temp = circle_coords.copy()
        c_temp[:, 0] = -c_temp[:, 0]
        circle_coords = np.concatenate([c_temp, circle_coords], 0)
        self.circle_coords = np.concatenate([-circle_coords, circle_coords], 0)

    def tick(self, dt: float, fov: np.ndarray) -> None:
        """
        'tick' function; updates internal state

        :param dt: time since last frame in s
        :param fov: targets within fov (passed from main)
        :return: None
        """
        super().tick(dt, fov)
        self.update_history(fov)
        self.explore(dt, fov)

    def explore(self, dt, fov):
        """
        'explore' function; steers the aircraft such that (in order of priority):
         - balloons are avoided
         - ground/ceiling are avoided
         - as much area as possible is discovered

        :param dt: time since last frame in s
        :param fov: targets within fov (passed from main)
        :return: None
        """
        d_nearest_target = 9999999
        rotation_matrix = np.array([[ math.cos((-self.pitch) * math.pi / 180),
                                     -math.sin((-self.pitch) * math.pi / 180)],
                                    [ math.sin((-self.pitch) * math.pi / 180),
                                      math.cos((-self.pitch) * math.pi / 180)]])
        evade_direction = 0

        for target in fov:
            d = np.matmul((target[:2]-self.rot_rect.center), rotation_matrix)
            self.nearest_target_pos_abs = d
            if (0 < d[0] < self.perception_front_dims[0]) and d[0] < d_nearest_target:
                if 0 < d[1] < self.perception_front_dims[1]:
                    evade_direction = 1
                elif 0 < -d[1] < self.perception_front_dims[1]:
                    evade_direction = -1

        if evade_direction != 0:
            self.adjust_pitch(dt*evade_direction)
        else:
            if self.orientation == 1 and (-0.9 > self.v_uv[0]):
                self.flip()
            elif self.orientation==-1 and (0.9 < self.v_uv[0]):
                self.flip()
            if self.pos_virtual[1] + self.v_uv[1] * 150 > 625 and (self.v_uv[1] >= -0.2):
                self.action = 'floor'
                if self.v_uv[0] > 0:
                    self.adjust_pitch(dt)
                else:
                    self.adjust_pitch(-dt)
            elif self.pos_virtual[1] + self.v_uv[1] * 150 < 10 and (self.v_uv[1] <= 0.2):
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
                if len(best_circle)==1:
                    best_circle = best_circle[0]
                elif best == 0:
                    best_circle = np.average(np.where(self.history[0][:,:64] == 0), axis=1)*self.history_scale
                    best_circle -= self.pos_virtual
                    self.action = 'explore tiebreak'
                    best_circle[1] = -best_circle[1]
                else:
                    best_circle = best_circle[0]
                    pass  # TODO: gelijk aantal vakkies in de buut

                diff_head = (math.atan2(best_circle[0], best_circle[1]) -
                             math.atan2(self.v[0], self.v[1])) * 180 / math.pi

                if diff_head > 180:
                    diff_head -= 360
                elif diff_head < -180:
                    diff_head += 360
                if diff_head<0:
                    self.adjust_pitch(dt)
                elif diff_head>0:
                    self.adjust_pitch(-dt)

    def update_history(self, fov):
        """
        Updates the history matrix with:
         - history of position/pitch
         - history of fov
         - history of targets

        :param fov: np array with targets in fov, passed from main
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

    def diff_overlap_circle(self, offset:tuple[int, int]=(0, 0)):
        """
        Returns the logical and of the circle with radius `r_fov` and centre `offset`,
         and the unexplored area. Effectively returns the area that would be discovered
         if the agent were to move to `offset`

        :param offset: centre of circle
        :return: new area
        """
        d_agent_x = (self.do_x - self.pos_virtual[0]/self.history_scale + offset[0]/self.history_scale)
        d_agent_y = (self.do_y - self.pos_virtual[1]/self.history_scale + offset[1]/self.history_scale)
        in_fov = (np.sqrt(d_agent_x ** 2 + d_agent_y ** 2) < (self.r_fov/self.history_scale))
        return np.logical_and(in_fov, ~(self.history[0].astype(bool))).astype(int)
