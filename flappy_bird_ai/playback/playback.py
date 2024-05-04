import random

import pygame

import flappy_bird_app.bird as BIRD
import flappy_bird_app.pipe as PIPE

from flappy_bird_ai.playback.custom_cycle import custom_cycle
from flappy_bird_ai.playback.playback_pipes import PlaybackPipes
from flappy_bird_ai.player import Player
from flappy_bird_ai.settings import settings

from neat import PlaybackPlayers
from neat.settings import settings_handler


def overwrite_pipes(birds: list[Player]) -> None:
    """Overwrite all players' pipes attribute because the original app design is bad."""

    seed = random.randint(0,100)
    for bird in birds:
        bird.pipes = PlaybackPipes(seed)

def initialise_birds(birds: list[Player]) -> None:
    """Get all birds in the starting state."""

    for bird in birds:
        bird.start_state()


def playback() -> None:
    """Show playback of the result of running NEAT on Flappy Bird.
    
    Do not alter settings.py between running NEAT and running this.
    Switch between generations with the left and right arrow keys.
    Switch between Species with the up and down arrow keys.
    Switch between viewing one Species at a time and all at once with the spacebar.
    Slow down up or speed up the playback with the j and k keys.
    """

    # pygame setup
    width = 480
    game_height = 620
    floor_height = 0.04 * game_height
    screen = pygame.display.set_mode((width, game_height + floor_height))
    pygame.display.set_caption("Flappy Bird: NEAT")
    pygame.font.init()
    font_height = int(0.06 * game_height)
    score_font = pygame.font.Font(pygame.font.get_default_font(), font_height)
    stats_font = pygame.font.Font(pygame.font.get_default_font(), int(0.7 * font_height))
    clock = pygame.time.Clock()
    running = True
    base_speed = 60
    speed_multiplier = 1

    # Initialise sprites
    bg = pygame.image.load('./submodules/flappy_bird_app/resources/background.bmp')
    bg = pygame.transform.scale(bg, (width, game_height))
    bird_sprites = [pygame.image.load('./submodules/flappy_bird_app/resources/bird_1.bmp'), pygame.image.load('./submodules/flappy_bird_app/resources/bird_2.bmp'), pygame.image.load('./submodules/flappy_bird_app/resources/bird_3.bmp')]
    bird_sprites = [pygame.transform.scale(bird_sprite, (BIRD.RADIUS * 8/3 * game_height, BIRD.RADIUS * 2 * game_height)) for bird_sprite in bird_sprites]
    bird_sprite_numbers = custom_cycle([0, 1, 2, 1], 5)
    pipe_top_sprite = pygame.image.load('./submodules/flappy_bird_app/resources/pipe_top.bmp')
    pipe_bottom_sprite = pygame.image.load('./submodules/flappy_bird_app/resources/pipe_bottom.bmp')
    pipe_top_sprite = pygame.transform.scale(pipe_top_sprite, (PIPE.WIDTH * width, (1 - PIPE.MIN_HEIGHT - PIPE.GAP) * game_height))
    pipe_bottom_sprite = pygame.transform.scale(pipe_bottom_sprite, (PIPE.WIDTH * width, (1 - PIPE.MIN_HEIGHT - PIPE.GAP) * game_height))
    floor_sprite = pygame.image.load('./submodules/flappy_bird_app/resources/floor.bmp')
    floor_sprite = pygame.transform.scale(floor_sprite, (width, floor_height))
    floor_rect = floor_sprite.get_rect(topleft=(0,game_height))

    # Get the first birds
    handled_settings = settings_handler(settings, silent=True)
    playback_folder = handled_settings['playback_settings']['save_folder']
    player_args = handled_settings['player_args']
    birds = PlaybackPlayers(playback_folder, Player, player_args)
    overwrite_pipes(birds)
    initialise_birds(birds)

    # Run the 'game' loop
    while running:

        # Handle all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            # Key presses
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    birds.generation += 1
                    overwrite_pipes(birds)
                    initialise_birds(birds)
                elif event.key == pygame.K_LEFT:
                    birds.generation -= 1
                    overwrite_pipes(birds)
                    initialise_birds(birds)

                elif event.key == pygame.K_UP:
                    birds.species_no += 1
                    overwrite_pipes(birds)
                    initialise_birds(birds)
                elif event.key == pygame.K_DOWN:
                    birds.species_no -= 1
                    overwrite_pipes(birds)
                    initialise_birds(birds)
                
                elif event.key == pygame.K_SPACE:
                    birds.per_species = not birds.per_species
                    overwrite_pipes(birds)
                    initialise_birds(birds)

                elif event.key == pygame.K_j:
                    speed_multiplier = max(1, speed_multiplier // 2)
                elif event.key == pygame.K_k:
                    speed_multiplier *= 2


        visible_birds = [bird for bird in birds if not bird.is_dead]

        # Restart if all dead
        if len(visible_birds) == 0:
            overwrite_pipes(birds)
            initialise_birds(birds)
            visible_birds = birds

        # Move the birds
        for bird in visible_birds:
            bird.look()
            move = bird.think()
            bird.move(move)

        # Fill the screen to wipe last frame
        screen.blit(bg, (0,0))

        # Draw the pipes
        for item in visible_birds[0].pipes.items:
            pipe_top_rect = pipe_top_sprite.get_rect(bottomleft=(item.position * width, item.height * game_height))
            pipe_bottom_rect = pipe_bottom_sprite.get_rect(topleft=(item.position * width, item.bottom_height * game_height))
            screen.blit(pipe_top_sprite, pipe_top_rect)
            screen.blit(pipe_bottom_sprite, pipe_bottom_rect)

        # Draw the birds
        sprite_id = next(bird_sprite_numbers)
        for bird in visible_birds:
            bird_sprite_rotated = pygame.transform.rotate(bird_sprites[sprite_id], bird.angle)
            bird_sprite_rect = bird_sprite_rotated.get_rect(center=(bird.x * width, bird.position * game_height))
            screen.blit(bird_sprite_rotated, bird_sprite_rect)

        # Draw the floor
        screen.blit(floor_sprite, floor_rect)

        # Show the score (all remaining will have the same score)
        score = score_font.render(f'{visible_birds[0].score}', True, 'white')
        score_rect = score.get_rect(center=(width/2, 0.05 * game_height))
        screen.blit(score, score_rect)
                    
        # Show the gen
        gen = stats_font.render(f'Gen: {birds.generation}', True, 'white')
        gen_rect = gen.get_rect(topleft=(0.05 * width, 0.03 * game_height))
        screen.blit(gen, gen_rect)

        # Show the species_no
        if birds.per_species:
            species_no = stats_font.render(f'Species: {birds.species_no + 1}', True, 'white')
        else:
            species_no = stats_font.render('Species: All', True, 'white')
        species_no_rect = gen.get_rect(topleft=(0.05 * width, 0.1 * game_height))
        screen.blit(species_no, species_no_rect)

        # Show the speed
        speed = stats_font.render(f'Speed: {speed_multiplier}x', True, 'white')
        speed_rect = speed.get_rect(topright=(0.95 * width, 0.03 * game_height))
        screen.blit(speed, speed_rect)

        # Display the changes
        pygame.display.flip()
        
        # Advance to next frame at chosen speed
        clock.tick(base_speed * speed_multiplier)

    pygame.quit()