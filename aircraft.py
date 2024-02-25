import math
import string
import pygame
import numpy as np


class Aircraft:
    def __init__(self,
                 mass: float,  # Kg
                 engine_power: float,  # N
                 agility: float,  # mate waarin pitch kan veranderen (deg/dt denk ik?); constant vooralsnog
                 c_drag: float,
                 c_lift: float,
                 sprite: string,
                 init_throttle: float,
                 init_pitch: float,
                 init_v: tuple[float, float],
                 init_pos: tuple[int, int]):

        # constanten
        self.engine_power = engine_power
        self.agility = agility  # TODO 1: moment afhankelijk van AoA en v
        self.mass = mass
        self.c_drag = c_drag  # TODO 2: Cd afhankelijk van AoA
        self.c_lift = c_lift  # TODO 3: Cl afhankelijk van AoA

        # variabelen
        self.throttle = init_throttle
        self.pitch = init_pitch
        self.v = np.array(init_v)
        self.pos = np.array(init_pos)

        # afhankelijke variabelen (np containers)
        self.pitch_uv = np.array([0.0, 0.0])
        self.v_uv = np.array([0.0, 0.0])
        self.f_gravity = np.array([0.0, 9.81*mass])
        self.f_engine = np.array([0.0, 0.0])
        self.f_drag = np.array([0.0, 0.0])
        self.f_lift = np.array([0.0, 0.0])

        # sprite info
        self.sprite = pygame.image.load(sprite)
        self.rot_sprite = pygame.transform.scale_by(self.sprite, 0.05)
        self.sprite = pygame.transform.scale_by(self.sprite, 0.05)
        self.rot_rect = self.sprite.get_rect(center=init_pos)

    def tick(self, dt: float):
        self.pitch_uv[0] = math.cos(-math.pi / 180 * self.pitch)
        self.pitch_uv[1] = math.sin(-math.pi / 180 * self.pitch)

        self.f_engine = self.throttle * 0.1 * self.engine_power * self.pitch_uv / self.mass   # f = m * a

        v_head = np.dot(self.v, self.pitch_uv) / np.linalg.norm(self.pitch_uv)  # scalarprojectie
        norm_lift = self.c_lift * np.linalg.norm(v_head)**2  # Cl * r * (v^2)/2 * A -> C * (v^2)
        self.f_lift[0] = norm_lift * np.cos(-math.pi/180 * ((self.pitch + 90) % 360))  # dit kan met minder code maar dat maakt het vm minder efficient
        self.f_lift[1] = norm_lift * np.sin(-math.pi/180 * ((self.pitch + 90) % 360))

        ########################### dit is nattevingerwerk; comment weg als het niet werkt
        if np.linalg.norm(self.v) != 0:
            self.v_uv = self.v / np.linalg.norm(self.v)
        AoA_rad = np.arccos(np.dot(self.v_uv, self.pitch_uv))
        AoA_multiplier = 10
        ###########################

        norm_drag = self.c_drag * np.linalg.norm(self.v)**2
        if np.linalg.norm(self.v) != 0:
            self.f_drag = -norm_drag * self.v / np.linalg.norm(self.v) * (1+AoA_rad**2*AoA_multiplier)

        f_res = self.f_engine + self.f_gravity + self.f_drag + self.f_lift
        self.v += dt * f_res
        self.pos += self.v * dt
        self.rot_rect.centerx = self.pos[0]
        self.rot_rect.centery = self.pos[1]

    def adjust_pitch(self, dt: float):
        self.pitch = (self.pitch + self.agility * dt) % 360
        self.rot_sprite = pygame.transform.rotate(self.sprite, self.pitch)
        self.rot_rect = self.rot_sprite.get_rect(center=self.sprite.get_rect(center=self.rot_rect.center).center)


# sources:
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
# https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/drageq.html
