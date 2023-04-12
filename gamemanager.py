import time
import pygame

from constants import FPS
from setup import window, clock, FONT
from scenes import Menu, Game


class GameManager:
    def __init__(self):
        self.current_scene = Menu(self) # Set initial scene

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

            # Render
            # window.fill((0,0,0)) # not needed if scene is drawing own background
            self.current_scene.render(window)
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
