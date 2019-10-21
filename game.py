import pygame
from config import *
import sys
import time
from constants import *
from objects import *
from agent import *
import numpy as np

from pygame.locals import *

pygame.init()

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()

uy = 50
ly = 300

dbp = 400

birds = [Bird(), BirdAgent()]

pipes = [Pipe(uy, ly, width + dbp * i) for i in range(int(width / dbp))]

current_time = time.time()

score = 0

while True:

    jump = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            jump = True

    if len(birds) == 0:
        pygame.quit()
        sys.exit()

    for bird in birds:
        if isinstance(bird, BirdAgent):
            bird.take_action(pipes)
        else:
            if jump:
                bird.jump()
        for pipe in pipes:
            if bird.collide(pipe):
                bird.die(score)
                birds.remove(bird)
                break

        
    surface.fill(WHITE)

    if pipes[0].x < -pipes[0].width:
        score += 1
        pipes.pop(0)

    if pipes[len(pipes) - 1].x + dbp < width:
        uy += np.random.random() * 100 - 50
        ly += np.random.random() * 100 - 50
        pipes.append(Pipe(uy, ly, pipes[len(pipes) - 1].x + dbp))

    dt = time.time() - current_time

    for obj in birds + pipes:
        obj.update(dt)
        obj.draw(surface)

    current_time += dt
    pygame.display.update()
