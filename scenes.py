import pygame
from scene import Scene

from setup import BUNNY_SPRITESHEET


class Menu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # TODO: Add scene variables here

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Switching to GAME")
            self.game_manager.switch_scene(Game)

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((255,0,0))
        surface.blit(BUNNY_SPRITESHEET[0],(100,100))



class Game(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # TODO: Add scene variables here

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Switching to MENU")
            self.game_manager.switch_scene(Menu)

    def update(self, dt):
        pass

    def render(self, surface):
        surface.fill((0,255,0))
