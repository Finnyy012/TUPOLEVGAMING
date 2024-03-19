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
        self.highwaytothedangerzoneeeeee = np.array((50,20))
        self.d_low = 0
        self.d2 = 0

        # internal state
        self.history_scale = 10
        self.history = np.zeros((2, int(window_dimensions[0]/self.history_scale), int(window_dimensions[1]/self.history_scale)))

        # np wizardry
        self.r_fov = 150
        self.do_x, self.do_y = np.indices((int(window_dimensions[0]/self.history_scale),int(window_dimensions[1]/self.history_scale)))
        circle_coords = np.array(
            [[9, 0], [9, 1], [9, 2], [8, 3], [8, 4], [7, 5], [7, 6], [6, 7], [5, 7], [4, 8], [3, 8], [2, 9], [1, 9],
             [0, 9]])
        c2 = circle_coords.copy()
        c2[:, 0] = -c2[:, 0]
        circle_coords = np.concatenate([c2, circle_coords], 0)
        self.circle_coords = np.concatenate([-circle_coords, circle_coords], 0)

    def tick(self, dt: float, fov: np.ndarray) -> None:
        super().tick(dt, fov)
        self.update_history(fov)

        self.d_low = 9999999999
        self.d2 = 9999999999
        for ballon in fov:
            d = np.linalg.norm(np.cross(self.pitch_uv, self.pos_virtual - ballon[:2]))
            d2 = np.dot(ballon[:2] - self.pos_virtual, np.linalg.norm(self.pitch_uv))
            if (d < self.highwaytothedangerzoneeeeee[1]) & (0 < d2[0] < self.highwaytothedangerzoneeeeee[0]):
                self.d_low = d
                self.d2 = d2[0]
        self.explore(dt)

    def explore(self, dt):
        if self.orientation==1 and (170 < self.pitch < 190):
            self.flipdebeer()
        elif self.orientation==-1 and ((0 <= self.pitch < 10) or ((350 < self.pitch <= 360))):
            self.flipdebeer()
        if self.pos_virtual[1] > 500 and ((175 < self.pitch < 360) or self.pitch < 5):
            if self.pitch > 270:
                self.adjust_pitch(dt)
            else:
                self.adjust_pitch(-dt)
        elif self.pos_virtual[1] < 100 and ((170 > self.pitch > 0) or self.pitch > 350):
            if self.pitch > 90:
                self.adjust_pitch(dt)
            else:
                self.adjust_pitch(-dt)
        else:
            best = 0
            bestc = None
            for c in self.circle_coords:
                n = np.sum(self.kirkel(c))
                if n >= best:
                    best = n
                    bestc = c
            if best==0:
                pass  # TODO: naar dichtstbijzijnde unexplored tile
            diff_head = (
                                math.atan2(bestc[0], bestc[1]) -
                                math.atan2(self.v[0], self.v[1])
                        ) * 180 / math.pi
            if diff_head > 180:
                diff_head -= 360
            elif diff_head < -180:
                diff_head += 360
            if diff_head<0:
                self.adjust_pitch(dt)
            elif diff_head>0:
                self.adjust_pitch(-dt)

    def update_history(self, fov):
        self.history[0][int((self.rot_rect.centerx-1)/self.history_scale)][int((self.rot_rect.centery-1)/self.history_scale)] = self.pitch
        for x in fov:
            self.history[1][int(x[0]/self.history_scale)][int(x[1]/self.history_scale)] = x[2]
        self.history[0] += self.kirkel()

    def kirkel(self, offset:tuple[int,int]=(0,0)):
        d_agent_x = (self.do_x - self.pos_virtual[0]/self.history_scale + offset[0]/self.history_scale)
        d_agent_y = (self.do_y - self.pos_virtual[1]/self.history_scale + offset[1]/self.history_scale)
        in_fov = (np.sqrt(d_agent_x ** 2 + d_agent_y ** 2) < (self.r_fov/self.history_scale))
        return np.logical_and(in_fov, ~(self.history[0].astype(bool))).astype(int)

        # print(np.logical_and(in_fov, ~(self.history[0].astype(bool))).astype(int))
        # print(self.history[0].astype(int)[0])

        # in_fov = (np.sqrt(d_agent_x ** 2 + d_agent_y ** 2) < r_fov).astype(int)

        # note 2: misschien is eerst een cirkel maken en dan de overlap checken beter maar for now doe ik het even zo
        # note 3:
        # >> > H, W = 4, 5
        # >> > x, y = np.indices([H, W])
        # >> > m
        # array([[0., 0.5, 2., 4.5, 8.],
        #        [0.5, 1., 2.5, 5., 8.5],
        #        [2., 2.5, 4., 6.5, 10.],
        #        [4.5, 5., 6.5, 9., 12.5]])
        # >> > x
        # array([[0, 0, 0, 0, 0],
        #        [1, 1, 1, 1, 1],
        #        [2, 2, 2, 2, 2],
        #        [3, 3, 3, 3, 3]])
        # >> > y
        # array([[0, 1, 2, 3, 4],
        #        [0, 1, 2, 3, 4],
        #        [0, 1, 2, 3, 4],
        #        [0, 1, 2, 3, 4]])
        # Note 4: the missile knows where it is because it knows where it isnt


