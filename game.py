import neat
import pygame
import time
import os
import random


window_width = 500
window_height = 800

bird_images =  [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]
pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
background_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))


class Bird:
    images = bird_images
    max_rotation = 25
    rotation_velocity = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.images[0]

    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        displacement = self.velocity*self.tick_count + 1.5*self.tick_count**2

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -=2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity

    def draw(self, window):
        self.image_count += 1

        if self.image_count < self.animation_time:
            self.image = self.images[0]
        elif self.image_count < self.animation_time*2:
            self.image = self.images[1]
        elif self.image_count < self.animation_time*3:
            self.image = self.images[2]
        elif self.image_count < self.animation_time*4:
            self.image = self.images[1]
        elif self.image_count == self.animation_time*4 + 1:
            self.image = self.images[0]
            self.image_count = 0

        if self.tilt <= -80:
            self.image = self.images[1]
            self.image_count = self.animation_time*2

        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectange = rotated_image.get_rect(center=self.image.get_rect(topleft = (self.x, self.y)).center)
        window.blit(rotated_image, new_rectange.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

def draw_window(window, bird):
    window.blit(background_image, (0, 0))
    bird.draw(window)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    window = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        bird.move()
        draw_window(window, bird)

    pygame.quit()
    quit()

main()
