from objects import Bird
from nn import NeuralNetwork
import numpy as np
from constants import BLUE

class BirdAgent(Bird):
    def __init__(self, brain=None):
        super().__init__()
        self.brain = NeuralNetwork([7, 4, 4, 1]) if brain == None else brain
        self.fitness = 0
        self.color = BLUE

    def take_action(self, pipes):
        features = self.create_features(pipes)
        # print(self.brain.predict(np.transpose(features))[0][0])
        if(self.brain.predict(np.transpose(features))[0][0] > 0.5):
            self.jump()
        self.fitness += 1

    def create_features(self, pipes):

        for i in range(len(pipes) - 1):
            if pipes[i].x + pipes[i].width > self.x:
                return (pipes[i].x - self.x, pipes[i].uy - self.y, pipes[i].ly - self.y, pipes[i + 1].x - self.x, pipes[i + 1].uy - self.y, pipes[i + 1].ly - self.y, self.v)

    def die(self, score):
        self.fitness += score * 10000

    def mutate(self, mutation_rate=0.01):
        self.brain.mutate(mutation_rate)
        return self
    
    @staticmethod
    def crossover(bird1, bird2):
        return BirdAgent(NeuralNetwork.crossover(bird1.brain, bird2.brain))
