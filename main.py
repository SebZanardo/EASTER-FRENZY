import pygame
from gamemanager import GameManager


def main():
    pygame.init()
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()