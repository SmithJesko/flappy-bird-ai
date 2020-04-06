import neat
import pygame
import time
import os
import random


pygame.init()
pygame.font.init()
pygame.display.set_caption('Flappy Bird AI')

window_width = 500
window_height = 800

gen = 0
clock = None

bird_images =  [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]
pipe_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
base_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
background_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "background.png")))

stat_font = pygame.font.SysFont("comicsans", 40)


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


def draw_window(window, birds, pipes, base, score, gen, pipe_ind):
    window.blit(background_image, (0, 0))
    for pipe in pipes:
        pipe.draw(window)
    base.draw(window)
    for bird in birds:
        try:
            pygame.draw.line(window, (255,0,0), (bird.x+bird.image.get_width()/2, bird.y + bird.image.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].pipe_top.get_width()/2, pipes[pipe_ind].height), 5)
            pygame.draw.line(window, (0,0,255), (bird.x+bird.image.get_width()/2, bird.y + bird.image.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].pipe_bottom.get_width()/2, pipes[pipe_ind].bottom), 5)
        except:
            pass
        bird.draw(window)
    text = stat_font.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (window_width - 10 - text.get_width(), 10))
    text = stat_font.render("FPS: " + str(int(clock.get_fps())), 1, (255, 255, 255))
    window.blit(text, (window_width - 10 - text.get_width(), 40))
    text = stat_font.render("Gen: " + str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 10))
    text = stat_font.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
    window.blit(text, (10, 40))
    pygame.display.update()


def main(genomes, config):
    global gen
    global clock
    gen += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

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
                pygame.quit()
                quit()


        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.05

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        remove = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 2
            pipes.append(Pipe(600))

        for r in remove:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move()
        draw_window(window, birds, pipes, base, score, gen, pipe_ind)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)