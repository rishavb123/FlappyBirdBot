import pygame
from config import *
import sys
import time
from constants import *
from objects import *
from agent import *
import numpy as np

from pygame.locals import *
import dill as pickle

pygame.init()

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
font = pygame.font.SysFont(None, 20)

clock = pygame.time.Clock()

dbp = int(sys.argv[1]) if len(sys.argv) > 1 else 300 #400 is easy, 300 is medium, 250 is hard
opening_dist = int(sys.argv[2]) if len(sys.argv) > 2 else 200 #250 is easy, 200 is medium, 150 is hard

if len(sys.argv) > 3:
    Bird.a = int(sys.argv[3])
if len(sys.argv) > 4:
    Bird.jump_v = int(sys.argv[4])

generations = None if len(sys.argv) <= 5 else int(sys.argv[5])
population_size = 200

birds = [BirdAgent() for _ in range(population_size)]
best_bird = birds[0]

pipes = []

for i in range(int(width / dbp) + 1):
    uy = np.random.random() * (height - opening_dist)
    ly = np.random.random() * 50 - 25 + opening_dist + uy
    pipes.append(Pipe(uy, ly, width + dbp * i))

current_time = time.time()

show = True

score = 0
generation = 0

dead = []

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not best_bird in birds:
                best_bird = np.random.choice(birds)
            with open("agents/bird-" + str(dbp) + "-" + str(opening_dist) + "-" + str(Bird.a) + "-" + str(Bird.jump_v) + "-" + str(generation) + "-" + str(int(time.time())) + ".pkl", "wb") as f:
                pickle.dump(best_bird, f)
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key == K_s:
            show = not show

    if len(birds) == 0:
        pipes = []
        score = 0
        for i in range(int(width / dbp) + 1):
            uy = np.random.random() * (height - opening_dist)
            ly = np.random.random() * 50 - 25 + opening_dist + uy
            pipes.append(Pipe(uy, ly, width + dbp * i))
        dead.sort(key=lambda x:-x.fitness)
        parents = dead[:int(population_size / 20)]
        best_bird = parents[0]
        total_fitness = sum([parent.fitness for parent in parents])
        p = [parent.fitness / total_fitness for parent in parents]
        birds = [BirdAgent.crossover(np.random.choice(parents, p=p), np.random.choice(parents, p=p)).mutate() if i < population_size * 0.95 else BirdAgent() for i in range(population_size - 1)]
        best_bird = BirdAgent(best_bird.brain)
        birds.append(best_bird)
        dead = []
        generation += 1
        if generations != None and generation > generations:
            if not best_bird in birds:
                best_bird = np.random.choice(birds)
            with open("agents/bird-" + str(dbp) + "-" + str(opening_dist) + "-" + str(Bird.a) + "-" + str(Bird.jump_v) + "-" + str(generation) + "-" + str(int(time.time())) + ".pkl", "wb") as f:
                pickle.dump(best_bird, f)
            pygame.quit()
            sys.exit()

    for bird in birds:
        if isinstance(bird, BirdAgent):
            bird.take_action(pipes)
        
        for pipe in pipes:
            if bird.collide(pipe):
                bird.die(score)
                birds.remove(bird)
                dead.append(bird)
                break

        
    surface.fill(WHITE)

    if pipes[0].x < -pipes[0].width:
        score += 1
        pipes.pop(0)
        uy = np.random.random() * (height - opening_dist)
        ly = np.random.random() * 50 - 25 + opening_dist + uy
        pipes.append(Pipe(uy, ly, pipes[len(pipes) - 1].x + dbp))

    dt = time.time() - current_time

    for obj in birds + pipes:
        obj.update(dt)
        if show or isinstance(obj, Pipe):
            obj.draw(surface)

    if best_bird in birds:
        best_bird.draw(surface, PURPLE)

    current_time += dt

    if len(birds) > 0:
        surface.blit(font.render("Fitness: " + str(birds[0].fitness + score * 10000), True, BLACK), [10, 10])
    surface.blit(font.render("Generation: " + str(generation), True, BLACK), [10, 30])
    surface.blit(font.render("Score: " + str(score), True, BLACK), [10, 50])
    surface.blit(font.render("Left: " + str(len(birds)), True, BLACK), [10, 70])

    pygame.display.update()
