import time
import pygame

from constants import FPS, COLOUR_KEY
from setup import game_surface, window, clock, FONT, WINDOW_WIDTH, WINDOW_HEIGHT, MUSIC_SFX
from scenes import MainMenu, Game


class GameManager:
    def __init__(self):
        self.current_scene = MainMenu(self) # Set initial scene
        self.failed_fast_transform = False

    def run(self):
        prev_frame_time = time.perf_counter()
        while True:
            dt = time.perf_counter() - prev_frame_time
            prev_frame_time = time.perf_counter()

            # Input
            for event in pygame.event.get():
                self.check_for_quit(event)
                self.current_scene.handle_event(event)

            # Update
            fps_text = FONT.render(str(int(clock.get_fps())), True, (255,255,255))
            self.current_scene.update(dt)

            if self.current_scene.scene_change_event=="game":
                self.switch_scene(Game)
                pygame.mixer.Channel(7).play(MUSIC_SFX, loops=-1)
                continue
            elif self.current_scene.scene_change_event=="menu":
                self.switch_scene(MainMenu)
                continue

            # Render
            # window.fill((0,0,0)) # not needed if scene is drawing own background
            self.current_scene.render(game_surface)

            # Draw surfaces to window

            if not self.failed_fast_transform:
                try:
                    pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT), window)
                except pygame.error:
                    print("The size and depth of game_surface and window don't match!")
                    self.failed_fast_transform = True

            if self.failed_fast_transform:
                mid_surface = pygame.transform.scale(game_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
                window.blit(mid_surface, [0, 0])



            window.blit(fps_text, (0,0))

            clock.tick(FPS)
            pygame.display.flip()

    def check_for_quit(self, event):
        if event.type == pygame.QUIT:
            self.terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.terminate()

    def switch_scene(self, new_scene):
        self.current_scene = new_scene(self)

    def terminate(self):
        pygame.quit()
        raise SystemExit
