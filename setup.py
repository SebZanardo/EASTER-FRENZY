import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_CAPTION
from helper.spritesheet import SpriteSheet


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
BUNNY_SPRITESHEET = SpriteSheet("assets/player-Sheet.png", (64, 64), flip=True).slice_sheet()
BUNNY_ANIMATION = {"idle": [BUNNY_SPRITESHEET[i] for i in range(0,4)], "run":[BUNNY_SPRITESHEET[i] for i in range(4,8)]}

ENEMY_SPRITESHEET = SpriteSheet("assets/spider-Sheet.png", (64,64), flip=True).slice_sheet()
ENEMY_ANIMATION = {"run": [ENEMY_SPRITESHEET[i] for i in range(0,3)]}

EGG_SPRITESHEET = SpriteSheet("assets/egg-Sheet.png", (32, 32), (40,40)).slice_sheet()

NEST_SPRITE = SpriteSheet("assets/nest.png", (64,32), (128,64)).get_sprite(0,0)

# Load Audio
# TODO: Add audio
