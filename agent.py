from objects import Bird

class BirdAgent(Bird):
    def __init__(self):
        super().__init__()

    def take_action(self, pipes):
        features = self.create_features(pipes)

    def create_features(self, pipes):

        for i in range(len(pipes) - 1):
            if pipes[i].x + pipes[i].width > self.x:
                return (pipes[i].x - self.x, pipes[i].uy - self.y, pipes[i].ly - self.y, pipes[i + 1].x - self.x, pipes[i + 1].uy - self.y, pipes[i + 1].ly - self.y, self.v)

        return None