# Flappy Bird AI: NEAT
An application of my implementation of NEAT (https://github.com/RJW20/NEAT) to the game Flappy Bird.

## Configuration

### What the Bird can see:
- Distance to the front of the next pipe.
- Own vertical velocity.
- Vertical distance to the end of the top and bottom pipes (2 values).

### What the Bird can do:
Every frame the bird can either jump or not jump.

### Neural Network Structure:
There are 4 input nodes, 1 output node with sigmoid activation (activation > 0.5 => jump, otherwise don't jump) and no hidden layers.

### Fitness Function:
The number of frames the bird has been alive for.

### Results:
Ultimately Flappy Bird is a very simple game and is easily beaten by NEAT. This bird was created in only the 2nd generation and it would go on forever:

![bird_passing_1000](https://github.com/RJW20/flappy-bird-ai-NEAT/assets/99192767/13780178-1982-4647-a5e3-a17af21a665e)

The simplicity of the game can be easily demonstrated by looking at the Genome controlling this bird:

![genome](https://github.com/RJW20/flappy-bird-ai-NEAT/assets/99192767/cdd1547b-b033-4996-9279-94fd418f3695)

The inputs are in the order listed above (plus a bias node). We see that being further away from the bottom on the top pipe and being closer to (or more obviously below) the top of the bottom pipe both work to increase the decision to jump. Neither of the other two inputs were even required.

## If you want to run it yourself

### Basic Requirements:
1. [Python](https://www.python.org/downloads/).
2. [Poetry](https://python-poetry.org/docs/) for ease of installing the dependencies.

### Getting Started:
1. Clone or download the repo `git clone https://github.com/RJW20/flappy-bird-ai-NEAT.git`.
2. Download the submodules `git submodule update --init`.
3. Set up the virtual environment `poetry install`.

### Running the Algorithm:
1. Change any settings you want in `flappy_bird_ai/settings.py`. For more information on what they control see [here](https://github.com/RJW20/NEAT/blob/main/README.md). 
2. Run the algorithm `poetry run main`.
3. View the playback of saved history with `poetry run playback`. You can change the generation shown with the left/right arrow keys and increase or slow-down the playback speed with the k/j keys respectively.
