import pygame
from sys import exit

pygame.init()


screen = pygame.display.set_mode((800, 400))

while True:     # Loop to run the game, and to update it.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Event to close the game
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            print("Foi \n não")



    pygame.display.update()
