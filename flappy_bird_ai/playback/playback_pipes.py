import random

from flappy_bird_app.pipes import Pipes, INTERVAL
from flappy_bird_app.pipe import Pipe
import flappy_bird_app.pipe as PIPE

class PlaybackPipes(Pipes):
    """Extension of Population class which overloads the generation of new pipes
    and sets a seed for generating their height."""

    def __init__(self, seed:int) -> None:
        super().__init__()
        self.generator = random
        self.generator.seed(seed)

    def start_state(self) -> None:
        super().start_state()
        self.items[0].height = round(self.generator.uniform(PIPE.MIN_HEIGHT, 1 - PIPE.MIN_HEIGHT - PIPE.GAP) * 100) / 100

    def update(self) -> None:
        """Overload Pipes.update, appending pipes with height generated from a seed."""

        for pipe in self.items:
            pipe.update()

        if (end_pipe_position := self.items[-1].position) < 1:
            new_pipe = Pipe(end_pipe_position + INTERVAL)
            new_pipe.height = round(self.generator.uniform(PIPE.MIN_HEIGHT, 1 - PIPE.MIN_HEIGHT - PIPE.GAP) * 100) / 100
            self.items.append(new_pipe)

        if self.items[0].position < self.items[0].width * -1:
            self.items.popleft()   