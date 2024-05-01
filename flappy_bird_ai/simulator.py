from .player import Player
from .settings import simulation_settings


def simulate(player: Player) -> Player:
    """Run the player in its environment and assign it a fitness signifying how 
    well it performs.
    
    The assigned fitness must be positive (>=0).
    """

    GOAL_SCORE = simulation_settings['goal_score']

    player.start_state()

    fitness = 0     #fitness is just the number of frames alive for
    while not player.is_dead:
        player.look()
        move = player.think()
        player.move(move)

        fitness += 1

        if player.score == GOAL_SCORE:
            break

    player.best_score = player.score
    player.fitness = fitness
    return player