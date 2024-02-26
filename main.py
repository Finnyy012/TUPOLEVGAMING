import numpy as np
import pygame
import aircraft
import matplotlib.pyplot as plt

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.SysFont(None, 24)
player = aircraft.Aircraft(
    mass=12,
    engine_force=10,
    agility=100, 
    c_drag=0.002,
    c_lift=0.01,
    sprite="assets/sprite_republican_i16.png", 
    init_throttle=100,
    init_pitch=0, 
    init_v=(200.0, 0.0),
    init_pos=(screen.get_width() / 2, screen.get_height() / 2)
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if player.throttle < 100:
            player.throttle += dt*100
    if keys[pygame.K_s]:
        if player.throttle > 0:
            player.throttle -= dt*100
    if keys[pygame.K_a]:
        player.adjust_pitch(dt)
    if keys[pygame.K_d]:
        player.adjust_pitch(-dt)

    player.tick(dt)

    player.pos[0] = player.pos[0] % screen.get_width()
    player.pos[1] = player.pos[1] % screen.get_height()
    screen.blit(player.rot_sprite, player.rot_rect)

    center = np.array((screen.get_width() / 2, screen.get_height() / 2))
    pygame.draw.line(screen, "black", center, center + player.v)
    pygame.draw.line(screen, "red", center, center + player.f_engine)
    pygame.draw.line(screen, "green", center, center + player.f_lift)
    pygame.draw.line(screen, "blue", center, center + player.f_drag)
    pygame.draw.line(screen, "yellow", center, center + player.f_gravity)

    screen.blit(
        font.render(
            "throttle: " + str(player.throttle), 
            False, 
            "black"
        ), 
        (20, 20)
    )
    screen.blit(
        font.render(
            "pitch:    " + str(player.pitch), 
            False, 
            "black"
        ), 
        (20, 40)
    )
    screen.blit(
        font.render(
            "IAS: " + str(np.linalg.norm(player.v)),
            False, 
            "black"
        ), 
        (20, 60)
    )
    screen.blit(
        font.render(
            "altitude: " + str(player.pos[1]),
            False,
            "black"
        ),
        (20, 80)
    )
    screen.blit(
        font.render(
            "AoA: " + str(player.AoA_deg),
            False,
            "black"
        ),
        (20, 100)
    )
    screen.blit(
        font.render(
            str(np.linalg.norm(player.f_drag)),
            False,
            "black"
        ),
        (20, 120)
    )

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0
#
# myimage = pygame.image.load("assets/sprite_republican_i16.png")
# myimage = pygame.transform.scale_by(myimage, 0.1)
# myimage = pygame.transform.rotate(myimage, 270)
#
# targetimg = pygame.image.load("assets/asterisk.png")
# targetimg = pygame.transform.scale_by(targetimg, 0.05)
# # trgtrect = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 + 1)
# trgtrect = targetimg.get_rect(center=targetimg.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 200)).center)
#
#
# # imagerect = myimage.get_rect()
#
# imagerect = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# v = [0.0, 0.0]
# a = 0.02
# alpha = 0
#
# def rot_center(image, angle, x, y):
#     rotated_image = pygame.transform.rotate(image, angle)
#     new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
#
#     return rotated_image, new_rect
#
# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")
#
#     imagerect.x += 300 * v[0] * dt
#     imagerect.y += 300 * v[1] * dt
#     imagerect.x = imagerect.x % screen.get_width()
#     imagerect.y = imagerect.y % screen.get_height()
#     # rotated_image = pygame.transform.rotate(myimage, o) #(math.pi/180)*
#     rotated_image, rotated_imagerect = rot_center(myimage, alpha, imagerect.x, imagerect.y)
#
#     # pygame.draw.circle(screen, "red", player_pos, 40)
#     screen.blit(targetimg, trgtrect)
#     screen.blit(rotated_image, rotated_imagerect)
#
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         # player_pos.y -= 300 * dt
#         # v[1] -= a * dt
#         v[0] += a * math.cos((math.pi/180) * alpha) #v0/a = cos(alpha) -> v0 = a*cos(alpha)
#         v[1] -= a * math.sin((math.pi / 180) * alpha)  # v1/a = sin(alpha) -> v1 = a*sin(alpha)
#     if keys[pygame.K_s]:
#         # player_pos.y += 300 * dt
#         # v[1] += a * dt
#         v[0] -= a * math.cos((math.pi / 180) * alpha)
#         v[1] += a * math.sin((math.pi / 180) * alpha)
#     if keys[pygame.K_q]:
#         # player_pos.y -= 300 * dt
#         # v[1] -= a * dt
#         v[0] += a * math.cos((math.pi/180) * (alpha + 90))  # v0/a = cos(alpha) -> v0 = a*cos(alpha)
#         v[1] -= a * math.sin((math.pi/180) * (alpha + 90))  # v1/a = sin(alpha) -> v1 = a*sin(alpha)
#     if keys[pygame.K_e]:
#         # player_pos.y += 300 * dt
#         # v[1] += a * dt
#         v[0] -= a * math.cos((math.pi / 180) * (alpha + 90))
#         v[1] += a * math.sin((math.pi / 180) * (alpha + 90))
#     if keys[pygame.K_a]:
#         # player_pos.x -= 300 * dt
#         # v[0] -= a * dt
#         alpha = (alpha + 300 * dt) % 360
#     if keys[pygame.K_d]:
#         # player_pos.x += 300 * dt
#         # v[0] += a * dt
#         alpha = (alpha - 300 * dt) % 360
#
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000
#
# pygame.quit()
#
