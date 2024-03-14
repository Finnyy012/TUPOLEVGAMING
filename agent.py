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
        self.d2    = 0

        # internal state
        self.history = np.zeros((2, window_dimensions[0], window_dimensions[1]))

        # np wizardry
        self.do_x, self.do_y = np.indices(window_dimensions)

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

    def explore(self):
        pass

    def update_history(self, fov):
        self.history[0][self.rot_rect.centerx-1][self.rot_rect.centery-1] = self.pitch
        for x in fov:
            self.history[1][x[0]][x[1]] = x[2]
        self.kirkel()

    def kirkel(self):
        d_agent_x = self.do_x - self.pos_virtual[0]
        d_agent_y = self.do_y - self.pos_virtual[1]
        in_fov = (np.sqrt(d_agent_x ** 2 + d_agent_y ** 2) < self.r_fov)
        self.history[0] += np.logical_and(in_fov, ~(self.history[0].astype(bool))).astype(int)

        # print(np.logical_and(in_fov, ~(self.history[0].astype(bool))).astype(int))
        # print(self.history[0].astype(int)[0])

        #in_fov = (np.sqrt(d_agent_x ** 2 + d_agent_y ** 2) < r_fov).astype(int)

        #note 1: Joris dreigt met huiselijk geweld als ik dit niet implementeer, dit kan echter effifienter dus vandaar gaat dit in een losse functie zodat het er later uit gesloopt kan worden
        #note 2: misschien is eerst een cirkel maken en dan de overlap checken beter maar for now doe ik het even zo
        #note 3:
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


