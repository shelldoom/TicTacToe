import pygame
import pygame.font
import sys
import random
from helper import *
pygame.init()

size = resX, resY = 800, 600
FPS = 30

screen = pygame.display.set_mode(size)
pygame.display.set_caption("test")
clock = pygame.time.Clock()

# Change below to True, if you to give Player the first chance
givePlayerFirstChance = False

# 3x3 tic tac
rows, cols = 3, 3
grid = Grid(rows, cols, 100, 100)
winner = False
gameOver = False
gameOverText = ''
ai, player = 'O', 'X'
player_chance = givePlayerFirstChance
reset = False

while 1:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset = True

    screen.fill(0)
    grid.draw_grid(screen)

    if not grid.winner_status():
        # If nobody has won, give ai/player a chance
        if player_chance:
            # Player has the chance, wait for player to make a valid move
            chance_text = pygame.font.SysFont(None, 60).render('Your chance!', 1, pygame.Color("forestgreen"))
            screen.blit(chance_text, chance_text.get_rect(center=(resX//2, chance_text.get_height() + 20)))
            if pygame.mouse.get_pressed()[0]:
                i, j = grid.get_cell_position(*pygame.mouse.get_pos())
                if i is not None:
                    # Player has made a valid move, and hence grid is updated
                    if grid.grid[i][j] == '':
                        grid.set(i, j, player)
                        player_chance = False
        else:
            # AI's chance
            chance_text = pygame.font.SysFont(None, 60).render('AI', 1, pygame.Color("firebrick"))
            screen.blit(chance_text, chance_text.get_rect(center=(resX//2, chance_text.get_height() + 20)))

            # Depth affects AI's move
            # Higher the depth, more better the move AI makes
            # But higher depth will result in slower respone time, especially for larger grids
            score, best_move = miniMax(grid, ai, player, depth=9)
            pygame.display.flip()
            # Random Delays for AI's moves, comment this if depth is higher or if grid is larger
            pygame.time.wait(random.randint(1500, 3000))
            grid.set(best_move[0], best_move[1], ai)
            player_chance = True
    else:
        # Game over
        gameOver=True
        winner = grid.winner_status()
        if winner == 'Tie': 
            gameOverText = 'Tie'
        else: 
            gameOverText = f"{'AI' if winner == ai else 'Player'} won!"

    if gameOver:
        gameOver_text = pygame.font.SysFont(None, 50).render(gameOverText, 1, pygame.Color("Coral"))
        screen.blit(gameOver_text, gameOver_text.get_rect(center=(resX//2, 50)))
        restart_text = pygame.font.SysFont(None, 50).render('Press R to restart', 1, pygame.Color("aquamarine3"))
        screen.blit(restart_text, restart_text.get_rect(center=(resX//2, resY//2 + 250)))

    if reset:
        # Reset the game
        grid.reset()
        winner = False
        gameOver = False
        gameOverText = ''
        ai, player = 'O', 'X'
        # player_chance = givePlayerFirstChance
        player_chance = random.choice([True, False])
        screen.fill(0)
        grid.draw_grid(screen)
        pygame.display.flip()
        reset = False
    
    pygame.display.flip()

