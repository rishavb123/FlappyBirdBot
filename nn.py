import numpy as np

class NeuralNetwork:

    def __init__(self, shape, ):
        self.weights = []
        self.biases = []
        self.shape = shape
        for i in range(len(shape) - 1):
            self.weights.append(np.random.random([shape[i + 1], shape[i]]) * 2 - 1)
            self.biases.append(np.random.random(shape[i + 1]) * 2 - 1)

    def forward(self, inp):
        result = inp
        for weight, bias in zip(self.weights, self.biases):
            result = NeuralNetwork.activation(np.add(np.matmul(weight, result), bias))

        return result

    def manyForward(self, inputs):
        return [self.forward(inp) for inp in inputs]

    def mutate(self, mutation_rate):
        for weight, bias in zip(self.weights, self.biases):
            for i in range(len(weight)):
                for j in range(len(weight[i])):
                    if np.random.random() < mutation_rate:
                        weight[i][j] = weight[i][j] + np.random.random() * 0.5 - 0.25

            for i in range(len(bias)):
                if np.random.random() < mutation_rate:
                    bias[i] = np.random.random() * 2 - 1
        return self

    @staticmethod
    def activation(x):
        return [xi if xi > 0 else 0 for xi in x]
        # return 1 / (1 + np.exp(-x))


    @staticmethod
    def crossover(nn1, nn2):
        if nn1.shape != nn2.shape:
            return None
        nn = NeuralNetwork(nn1.shape)
        for i in range(len(nn1.weights)):
            nn.weights[i] = np.add(nn1.weights[i], nn2.weights[i]) / 2
            nn.biases[i] = np.add(nn1.biases[i], nn2.biases[i]) / 2
        return nn

    @staticmethod
    def clone(nn):
        nn2 = NeuralNetwork(nn.shape)
        for i in range(len(nn.weights)):
            nn2.weights[i] = nn.weights[i].copy()
            nn2.biases[i] = nn.biases[i].copy()
        return nn