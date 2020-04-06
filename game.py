import neat
import pygame
import time
import os
import random


pygame.font.init()

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

stat_font = pygame.font.SysFont("comicsans", 50)


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


class Pipe:
    gap = 200
    velocity = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_image, False, True)
        self.pipe_bottom = pipe_image

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(40, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.pipe_top, (self.x, self.top))
        window.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        top_point = bird_mask.overlap(top_mask, top_offset)

        if top_point or bottom_point:
            return True

        return False


class Base:
    velocity = 5
    width = base_image.get_width()
    image = base_image

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, window):
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))


def draw_window(window, bird, pipes, base, score):
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    base.draw(window)
    bird.draw(window)
    text = stat_font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (window_width - 10 - text.get_width(), 10))
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    score = 0
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        add_pipe = False
        remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in remove:
            pipes.remove(r)

        if bird.y + bird.image.get_height() > 730:
            pass

        base.move()
        draw_window(window, bird, pipes, base, score)

    pygame.quit()
    quit()

main()
