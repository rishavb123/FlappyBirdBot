from nn import NeuralNetwork
import numpy as np

population_size = 100
num_of_generations = 1000
shape = [2, 2, 1]

def fitness(nn, log=False):
    inputs = [[0, 0], [1, 0], [0, 1], [1, 1]]
    targets = [[0], [1], [1], [0]]
    outputs = nn.manyForward(inputs)

    if log:
        print("Starting Fitness: ")
        print(outputs, targets)

    cost = np.subtract(targets, outputs)

    if log:
        print(cost)

    cost = sum(np.multiply(cost, cost))

    if log:
        print(cost)

    return 1/cost[0]

def softmax(fitnesses):
    return [np.exp(f) / sum(np.exp(fitnesses)) for f in fitnesses]


def test():
    nn = NeuralNetwork(shape)
    print("0", nn.forward([0, 0]))
    print("fitness", fitness(nn), "\n")
    for i in range(10):
        nn.mutate(1)
        print("0", nn.forward([0, 0]))
        print("fitness", fitness(nn), "\n")

def main():
    population = []
    for i in range(population_size):
        population.append(NeuralNetwork(shape))

    for i in range(num_of_generations):
        population = sorted(population, key=(lambda network: fitness(network)))
        fitnesses = softmax([fitness(nn) for nn in population])
        new_population = []
        for i in range(population_size):
            new_population.append(np.random.choice(population, p=fitnesses).mutate(0.1))
            # new_population.append(NeuralNetwork.crossover(np.random.choice(population, p=fitnesses), np.random.choice(population, p=fitnesses)).mutate(0.01))
        population = new_population

    print(population[0].forward([0, 0]))
    print(population[0].forward([1, 0]))
    print(population[0].forward([0, 1]))
    print(population[0].forward([1, 1]))

main()