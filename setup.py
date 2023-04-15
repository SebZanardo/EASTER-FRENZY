import pygame

from constants import SURFACE_WIDTH, SURFACE_HEIGHT, WINDOW_CAPTION, COLOUR_KEY
from helper.spritesheet import SpriteSheet


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
SCORE_FONT = pygame.font.Font("assets/nokiafc22.ttf", 30)
TITLE_FONT = pygame.font.Font("assets/nokiafc22.ttf", 50)
BUTTON_FONT = pygame.font.Font("assets/nokiafc22.ttf", 30)

# Load Images, Spritesheets and Animations
BUNNY_SPRITESHEET = SpriteSheet("assets/player-Sheet.png", (64, 64), flip=True).slice_sheet()
BUNNY_ANIMATION = {"idle": [[BUNNY_SPRITESHEET[i] for i in range(0,4)],   [BUNNY_SPRITESHEET[15], BUNNY_SPRITESHEET[15]]  ], "run":[[BUNNY_SPRITESHEET[i] for i in range(4,10)],    [BUNNY_SPRITESHEET[i] for i in range(15,20)]], "dash":[  [BUNNY_SPRITESHEET[10], BUNNY_SPRITESHEET[10]]  ], "game over":[ [BUNNY_SPRITESHEET[i] for i in range(20, 26)] ]}
BUNNY_DASH_SPRITES = [BUNNY_SPRITESHEET[i] for i in range(11, 15)]

ENEMY_SPRITESHEET = SpriteSheet("assets/spider-Sheet.png", (64,64), flip=True).slice_sheet()
ENEMY_ANIMATION = {"run": [ENEMY_SPRITESHEET[i] for i in range(0,4)], "carry": [ENEMY_SPRITESHEET[i] for i in range(4,8)], "hit": [ENEMY_SPRITESHEET[8], ENEMY_SPRITESHEET[0]], "scatter": [ENEMY_SPRITESHEET[i] for i in range(9,13)]}

EGG_SPRITESHEET = SpriteSheet("assets/egg-Sheet.png", (32, 32), (40,40)).slice_sheet()
EGG_SPRITESHEET[len(EGG_SPRITESHEET)]=pygame.transform.scale( pygame.image.load("assets/grey-egg.png").convert_alpha(), (40,40))
BOOMERANG_SPRITESHEET = SpriteSheet("assets/boomerang-Sheet.png", (32,32), (46, 46)).slice_sheet()

NEST_SPRITE = pygame.transform.scale(pygame.image.load("assets/nest.png").convert_alpha(), (128,64))
SHADOW_SPRITE = pygame.image.load("assets/shadow.png").convert_alpha()
BLOOD_PARTICLES = SpriteSheet("assets/blood-Sheet.png", (16, 16), (32,32)).slice_sheet()
PARTCILES = SpriteSheet("assets/particle-Sheet.png", (7,7))

SCORE_PARTICLE_SPRITES = [ FONT.render("+10", 0, (255,255,255)), FONT.render("+20", 0, (255,255,255))  ]

CROSSHAIR_SPRITE = pygame.transform.scale(pygame.image.load("assets/crosshair.png").convert_alpha(), (15, 15))
COVER_ART = pygame.transform.scale(pygame.image.load("assets/cover_art.png").convert_alpha(), (SURFACE_WIDTH, SURFACE_HEIGHT))

VIGNETTE = pygame.transform.scale(pygame.image.load("assets/vignette.png").convert_alpha(), (SURFACE_WIDTH, SURFACE_HEIGHT))

PARTICLE_SPRITES = SpriteSheet("assets/particle-Sheet.png", (7, 7), (7,7)).slice_sheet()

STAR_PARTICLE_SPRITE = PARTICLE_SPRITES[7]




#Sounds
PLAYER_WALK_SFX = pygame.mixer.Sound("assets/sfx/walk_sfx.wav")
PLAYER_WALK_SFX.set_volume(0.4)

ENEMY_DEATH_SFX = (pygame.mixer.Sound("assets/sfx/death_sfx_1.wav"), pygame.mixer.Sound("assets/sfx/death_sfx_2.wav"))
for i in range(2): ENEMY_DEATH_SFX[i].set_volume(0.6)

THROW_SFX = pygame.mixer.Sound("assets/sfx/throw_sfx.wav")
THROW_SFX.set_volume(0.6)

BOOMERANG_SFX = pygame.mixer.Sound("assets/sfx/boomerang_sfx.wav")
BOOMERANG_SFX.set_volume(0.1)

DASH_SFX = pygame.mixer.Sound("assets/sfx/dash_sfx.wav")
DASH_SFX.set_volume(0.5)

MUSIC_SFX = pygame.mixer.Sound("assets/sfx/game_music.wav")
MUSIC_SFX.set_volume(0.4)



#Buttons
BUTTON_BASE = pygame.transform.scale( pygame.image.load("assets/button_base.png"), (128, 50))   .convert_alpha()

PLAY_BUTTON = BUTTON_BASE.copy()

temp_text=BUTTON_FONT.render("PLAY", False, (255,255,255))
PLAY_BUTTON.blit(temp_text, temp_text.get_rect(center=BUTTON_BASE.get_rect().center ))

