from flappy_bird_app import Bird
from flappy_bird_app.bird import MAX_VELOCITY
from neat import BasePlayer


class Player(Bird, BasePlayer):

    def __init__(self, **player_args: dict) -> None:
        super().__init__()
        self.vision: list[float]
        self.best_score: int = 0

    def look(self) -> None:
        """Set the bird's vision.
        
        Can see: distance to the pipe, own vertical velocity, vertical distance 
        to the end of the top of the pipe, vertical distance to the end of the 
        bottom of the pipe.
        """

        front_pipe = self.pipes.items[0]
        if self.x - self.radius > front_pipe.position + front_pipe.width:
            front_pipe = self.pipes.items[1]
        self.vision = [
            max((front_pipe.position - self.x)/(1 - self.x), 0), 
            self.velocity/MAX_VELOCITY,
            max(self.position - front_pipe.height,0), 
            max(front_pipe.bottom_height - self.position,0)
        ]

    def think(self) -> int:
        """Feed the input into the Genome and return the output as a valid move."""
        return self.genome.propagate(self.vision)[0]