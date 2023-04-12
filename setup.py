import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION
from spritesheet import SpriteSheet


pygame.init()

# Setup Pygame
monitor = pygame.display.Info()
#window = pygame.display.set_mode((monitor.current_w, monitor.current_h), flags=pygame.FULLSCREEN)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()

# Load Fonts
FONT = pygame.font.Font("assets/nokiafc22.ttf", 20)

# Load Images, Spritesheets and Animations
BUNNY_SPRITESHEET = SpriteSheet("assets/player-Sheet.png", 64, 64).slice_sheet()

# Load Audio
# TODO: Add audio
