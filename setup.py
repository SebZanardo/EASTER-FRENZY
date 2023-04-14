import pygame

from constants import SURFACE_WIDTH, SURFACE_HEIGHT, WINDOW_CAPTION, COLOUR_KEY
from spritesheet import SpriteSheet


pygame.init()

# Setup Pygame
monitor = pygame.display.Info()

MONITOR_WIDTH, MONITOR_HEIGHT = monitor.current_w, monitor.current_h

monitor_aspect = MONITOR_WIDTH/MONITOR_HEIGHT
surface_aspect = SURFACE_WIDTH/SURFACE_HEIGHT
#upscale surface to fit monitor
if monitor_aspect>surface_aspect:
  WINDOW_WIDTH, WINDOW_HEIGHT = (MONITOR_HEIGHT/SURFACE_HEIGHT)*SURFACE_WIDTH, MONITOR_HEIGHT
else:
  WINDOW_WIDTH, WINDOW_HEIGHT = MONITOR_WIDTH, (MONITOR_WIDTH/SURFACE_WIDTH)*SURFACE_HEIGHT

game_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

SCALE_FACTOR=SURFACE_WIDTH/WINDOW_WIDTH

pygame.display.set_caption(WINDOW_CAPTION)
clock = pygame.time.Clock()

# Load Fonts
FONT = pygame.font.Font("assets/nokiafc22.ttf", 20)

# Load Images, Spritesheets and Animations
BUNNY_SPRITESHEET = SpriteSheet("assets/player-Sheet.png", (64, 64), flip=True).slice_sheet()
BUNNY_ANIMATION = {"idle": [BUNNY_SPRITESHEET[i] for i in range(0,4)], "run":[BUNNY_SPRITESHEET[i] for i in range(4,10)], "dash":[BUNNY_SPRITESHEET[10], BUNNY_SPRITESHEET[10]]}
BUNNY_DASH_SPRITES = [BUNNY_SPRITESHEET[i] for i in range(11, 15)]

ENEMY_SPRITESHEET = SpriteSheet("assets/spider-Sheet.png", (64,64), flip=True).slice_sheet()
ENEMY_ANIMATION = {"run": [ENEMY_SPRITESHEET[i] for i in range(0,4)], "carry": [ENEMY_SPRITESHEET[i] for i in range(4,8)], "hit": [ENEMY_SPRITESHEET[8], ENEMY_SPRITESHEET[0]], "scatter": [ENEMY_SPRITESHEET[i] for i in range(9,13)]}

EGG_SPRITESHEET = SpriteSheet("assets/egg-Sheet.png", (32, 32), (40,40)).slice_sheet()
BOOMERANG_SPRITESHEET = SpriteSheet("assets/boomerang-Sheet.png", (32, 32)).slice_sheet()

NEST_SPRITE = pygame.transform.scale(pygame.image.load("assets/nest.png").convert_alpha(), (128,64))
SHADOW_SPRITE = pygame.image.load("assets/shadow.png").convert_alpha()
BLOOD_PARTICLES = SpriteSheet("assets/blood-Sheet.png", (16, 16), (32,32)).slice_sheet()
PARTCILES = SpriteSheet("assets/particle-Sheet.png", (7,7))

CROSSHAIR_SPRITE = pygame.transform.scale(pygame.image.load("assets/crosshair.png").convert_alpha(), (15, 15))
COVER_ART = pygame.transform.scale(pygame.image.load("assets/cover_art.png").convert_alpha(), (SURFACE_WIDTH, SURFACE_HEIGHT))

VIGNETTE = pygame.transform.scale(pygame.image.load("assets/vignette.png").convert_alpha(), (SURFACE_WIDTH, SURFACE_HEIGHT))

# Load Audio
# TODO: Add audio
