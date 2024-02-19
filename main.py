# Example file showing a circle moving on screen
import math

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

myimage = pygame.image.load("assets/cursor.png")
myimage = pygame.transform.scale_by(myimage, 0.1)
myimage = pygame.transform.rotate(myimage, 270)

# imagerect = myimage.get_rect()

imagerect = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
v = [0.0, 0.0]
a = 0.02
alpha = 0

def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    imagerect.x += 300 * v[0] * dt
    imagerect.y += 300 * v[1] * dt
    # rotated_image = pygame.transform.rotate(myimage, o) #(math.pi/180)*
    rotated_image, rotated_imagerect = rot_center(myimage, alpha, imagerect.x, imagerect.y)

    # pygame.draw.circle(screen, "red", player_pos, 40)
    screen.blit(rotated_image, rotated_imagerect)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        # player_pos.y -= 300 * dt
        # v[1] -= a * dt
        v[0] += a * math.cos((math.pi/180) * alpha) #v0/a = cos(alpha) -> v0 = a*cos(alpha)
        v[1] -= a * math.sin((math.pi / 180) * alpha)  # v1/a = sin(alpha) -> v1 = a*sin(alpha)
    if keys[pygame.K_s]:
        # player_pos.y += 300 * dt
        # v[1] += a * dt
        v[0] -= a * math.cos((math.pi / 180) * alpha)
        v[1] += a * math.sin((math.pi / 180) * alpha)
    if keys[pygame.K_a]:
        # player_pos.x -= 300 * dt
        # v[0] -= a * dt
        alpha = (alpha + 300 * dt) % 360
    if keys[pygame.K_d]:
        # player_pos.x += 300 * dt
        # v[0] += a * dt
        alpha = (alpha - 300 * dt) % 360

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()


