import pygame
from config import *
import sys
import time
from constants import *
from objects import *
from agent import *
import numpy as np
import os

from pygame.locals import *
import dill as pickle

pygame.init()

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,20)

dbp = int(sys.argv[1]) if len(sys.argv) > 1 else 300 #400 is easy, 300 is medium, 250 is hard
opening_dist = int(sys.argv[2]) if len(sys.argv) > 2 else 200 #250 is easy, 200 is medium, 150 is hard

if len(sys.argv) > 3:
    Bird.a = int(sys.argv[3])
if len(sys.argv) > 4:
    Bird.jump_v = int(sys.argv[4])

birds = [Bird()]

agent_file_name = "./agents/none.pkl"
load_model = False

for root, dirs, files in os.walk("./agents/"):
    if len(files) > 0:
        name = agent_file_name.split("/")[len(agent_file_name.split("/")) - 1]
        if not name in files:
            for f in files:
                arr = [int(a) if a.isdigit() else a for a in f.split("-")]
                if arr[1] == dbp and arr[2] == opening_dist and arr[3] == Bird.a and arr[4] == Bird.jump_v:
                    agent_file_name = "./agents/" + f
                    load_model = True
        else:
            load_model = True


if load_model:
    with open(agent_file_name, "rb") as f:
        birds.append(pickle.load(f))
else:
    birds.append(BirdAgent())

pipes = []

for i in range(int(width / dbp) + 1):
    uy = np.random.random() * (height - opening_dist)
    ly = np.random.random() * 50 - 25 + opening_dist + uy
    pipes.append(Pipe(uy, ly, width + dbp * i))

current_time = time.time()

show = True

score = 0

dead = []

while True:

    jump = False

    for event in pygame.event.get():   

        if event.type == pygame.QUIT:
            print("Score:", score)
            pygame.quit()
            quit()         

        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            jump = True

        if event.type == KEYDOWN and event.key == K_s:
            show = not show

    if len(birds) == 0:
        print("Score:", score)
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

    current_time += dt

    surface.blit(font.render("Score: " + str(score), True, BLACK), [10, 10])
    pygame.display.update()
