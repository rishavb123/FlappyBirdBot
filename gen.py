from nn import NeuralNetwork

class GeneticAlgorithm:

    def __init__(self, shape, population_size = 100):
        self.population = []
        for i in range(population_size):
            self.population.append(NeuralNetwork(shape))

    def next_generate(self, fitness):
        best_networks = 0