import neat
import pygame
import time
import os
import random

win_width = 600
win_height = 800

bird_images =  [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]
pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
background_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))