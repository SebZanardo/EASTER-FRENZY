import pygame
import engine
import time

from constants import FPS
from setup import window, clock, FONT

pygame.init()


def main ():
    world = engine.world(window, [20,40], 1, 40)

    previous_time = time.perf_counter()

    while True:
        dt = calculate_dt(time.perf_counter(), previous_time)
        previous_time = time.perf_counter()

        # Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()

        pressed = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()

        # Update
        world.update(pressed, (mouse_pos[0], mouse_pos[1]), mouse_state, dt)

        # Render elements of the game
        window.fill((0,0,0))
        world.render()

        window.blit(FONT.render(str(int(clock.get_fps())), 0, (255,0,255)), (0,0))

        #rot_image=pygame.transform.rotate(image, angle)
        #WINDOW.blit(rot_image, rot_image.get_rect(center=image.get_rect().center ))

        pygame.display.flip()
        clock.tick(FPS)

def terminate():
    pygame.quit()
    raise SystemExit

def calculate_dt(current_time, previous_time):
    return current_time - previous_time

if __name__ == "__main__":
    main()
