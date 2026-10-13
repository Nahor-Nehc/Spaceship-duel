import pygame
import os
WIDTH, HEIGHT = 900, 500

# ship
VEL = 4
SPACESHIP_SIZE = (76, 68)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SPACESHIP_SIZE), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_SIZE)), 270)

# bullets
BULLET_VEL = 7
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
MAX_BULLETS = 6
BULLET_COLOUR = [(255, 0, 0), (255, 255, 0)]

# ammo
AMMO_BAR_WIDTH, AMMO_BAR_HEIGHT = 30, 280
YELLOW_AMMO_BAR = pygame.Rect(10, HEIGHT - BULLET_HEIGHT - 10, AMMO_BAR_WIDTH, BULLET_HEIGHT)
RED_AMMO_BAR = pygame.Rect(WIDTH - AMMO_BAR_WIDTH - 10, HEIGHT - BULLET_HEIGHT - 10, AMMO_BAR_WIDTH, BULLET_HEIGHT)

# other
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))