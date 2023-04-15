import pygame, random, math
from base_classes.scene import Scene
from constants import SURFACE_WIDTH, SURFACE_HEIGHT, MAP_SIZE, TILE_SIZE, CHECK_COLOURS
from helper.utils import clamp, update_and_remove
from base_classes.button import Button

from game_elements.camera import Camera
from game_elements.player import Player
from game_elements.enemy import Enemy
from game_elements.egg import Egg
from game_elements.nest import Nest
from game_elements.wave_spawner import WaveSpawner

from setup import SCALE_FACTOR, CROSSHAIR_SPRITE, FONT, SCORE_FONT, COVER_ART, VIGNETTE, EGG_SPRITESHEET, PLAY_BUTTON, TITLE_FONT, MUSIC_SFX


class MainMenu(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # TODO: Add scene variables here
        pygame.mouse.set_visible(True)

        self.background_tick=0

        self.title_text=TITLE_FONT.render("Easter Frenzy", False, (255,255,255))
        self.title_rect=self.title_text.get_rect( center=(SURFACE_WIDTH/2, SURFACE_HEIGHT/2-100)  )

        self.instruction_text = FONT.render("Press <ENTER> key to start", False, (255,255,255))
        self.instruction_text_rect = self.instruction_text.get_rect(center=(SURFACE_WIDTH/2, SURFACE_HEIGHT-50))

        self.play_button=Button((SURFACE_WIDTH/2, 200), PLAY_BUTTON, 1.1)

        self.mouse_event=False

        self.scene_change_event=None
        self.fade_tick=None

        self.fade_surf = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT), flags=pygame.SRCALPHA)
        self.fade_surf.fill( (0,0,0) )






    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print("Switching to GAME")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_event=True


    def update(self, dt):
        mouse_pos=pygame.mouse.get_pos()
        mouse_pos=(mouse_pos[0]*SCALE_FACTOR, mouse_pos[1]*SCALE_FACTOR)

        self.background_tick+=dt
        self.play_button.update(mouse_pos)

        if self.play_button.hover and self.mouse_event:
            self.fade_tick=0


        if self.fade_tick!=None:
            self.fade_tick+=dt
            self.fade_surf.set_alpha(min(self.fade_tick*500, 255  ))

            if self.fade_tick>1:
                self.scene_change_event="game"


        self.mouse_event=False


    def render(self, surface):
        surface.fill((255,0,0))

        for y in range(9):
            for x in range(18):
                pygame.draw.rect(surface, CHECK_COLOURS[int((x%2)-(y%2)==0)], pygame.Rect ((x-(self.background_tick)%2)* TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)  )


        surface.blit(VIGNETTE, (0,0))

        surface.blit(self.title_text, self.title_rect)

        self.play_button.render(surface)

        if self.fade_tick!=None:
            surface.blit(self.fade_surf, (0,0))








class Game(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.map_data = [[ int((x%2)-(y%2)==0) for x in range(MAP_SIZE[0])] for y in range(MAP_SIZE[1]) ]

        self.map_rect=pygame.Rect(0,0,MAP_SIZE[0]*TILE_SIZE, MAP_SIZE[1]*TILE_SIZE)

        self.surface_size=(SURFACE_WIDTH, SURFACE_HEIGHT)

        self.particles=([], [])
        self.eggs=[]
        self.enemies=[]

        self.nest_pos=self.map_rect.center

        self.pickup_event=False

        self.game_score=0
        self.game_score_render=0

        self.flash_tick=0

        self.game_over=False
        self.game_over_tick=None

        self.music_on=True


        self.active_cam=Camera(self.nest_pos, self.surface_size)
        self.active_player=Player( [self.nest_pos[0], self.nest_pos[1]-100], self.active_cam, self.particles, ((0,0), self.map_rect.bottomright))
        self.active_cam.follow_mode(self.active_player.pos, 4)
        self.active_cam.set_bounds((100,100), (self.map_rect.right-100, self.map_rect.bottom-100) )

        self.nest=Nest(self.nest_pos, self.active_cam, self.particles)
        for i in range(4): self.eggs.append(Egg([self.nest_pos[0]+i*25-36, self.nest_pos[1]-10], self.active_cam, self.particles, self.active_player, self.active_player.weapon, i, self.nest_pos))

        self.wave_spawner = WaveSpawner(self.nest_pos[0], self.nest_pos[1], 800, self.enemies, self.particles, self.active_cam, self.eggs, self.active_player.weapon, self.map_rect.bottomright)

        pygame.mouse.set_visible(False)
        self.crosshair_rect = CROSSHAIR_SPRITE.get_rect()

        self.scene_change_event=None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_f:
                self.pickup_event=True
            elif event.key==pygame.K_m:
                self.music_on = not self.music_on

                if self.music_on:
                    pygame.mixer.Channel(7).play(MUSIC_SFX, loops=-1)
                else:
                    pygame.mixer.Channel(7).pause()


    def update(self, dt):
        keys=pygame.key.get_pressed()

        mouse_pos=pygame.mouse.get_pos()
        mouse_pos=(mouse_pos[0]*SCALE_FACTOR, mouse_pos[1]*SCALE_FACTOR)
        mouse_state=pygame.mouse.get_pressed()



        if self.game_over:
            if keys[pygame.K_RETURN]:
                self.scene_change_event="game"


        else:
            self.crosshair_rect.center = mouse_pos

            self.active_player.update(keys, self.pickup_event, mouse_state, mouse_pos, dt)

            self.active_cam.update(mouse_pos, dt)


            if self.game_over_tick==None:
                game_over_flag=True
                for egg in self.eggs:
                    egg.update(self.pickup_event, dt)
                    if egg.state!=4:game_over_flag=False

                    self.game_score+=egg.score_return

                if game_over_flag:
                    self.active_player.state="game over"
                    self.active_player.weapon.state=2
                    self.active_player.anim_tick=0
                    self.active_player.holding_anim=0
                    self.game_over_tick=0
                    self.restart_prompt=SCORE_FONT.render("PRESS RETURN TO RESTART", 0, (255,255,255))
                    self.restart_prompt_rect = self.restart_prompt.get_rect(center=(SURFACE_WIDTH/2, SURFACE_HEIGHT/2)  )

            update_and_remove(self.particles[0], dt)
            update_and_remove(self.particles[1], dt)


            for i in range(len(self.enemies)-1,-1,-1):
                item=self.enemies[i]
                item.update(dt)
                if item.is_dead:
                    self.enemies.pop(i)
                    self.game_score+=10


            self.pickup_event=False

            if self.game_score_render!=self.game_score:self.game_score_render+=1

            self.flash_tick+=dt


            self.wave_spawner.update(dt)

            if self.game_over_tick!=None:
                self.game_over_tick+=dt
                if self.game_over_tick>2:
                    self.game_over=True
                    pygame.mouse.set_visible(True)






    def render(self, surface):
        surface.fill((20,20,20))
        clip_start=[ clamp(int(   self.active_cam.render_pos[0]/TILE_SIZE)-1, 0, MAP_SIZE[0] ) , clamp(int(self.active_cam.render_pos[1]//TILE_SIZE)-1, 0, MAP_SIZE[1])]
        clip_end=[  clamp( int(  (self.active_cam.render_pos[0]+self.surface_size[0])//TILE_SIZE)+1, 0, MAP_SIZE[0]), clamp(int(  (self.active_cam.render_pos[1]+self.surface_size[1])//TILE_SIZE )+1, 0, MAP_SIZE[1]) ]

        for y in range(clip_start[1], clip_end[1]):
            for x in range(clip_start[0], clip_end[0]):
                pygame.draw.rect(surface, CHECK_COLOURS[self.map_data[y][x]],
                                            pygame.Rect(x*TILE_SIZE-self.active_cam.render_pos[0], y*TILE_SIZE-self.active_cam.render_pos[1], TILE_SIZE, TILE_SIZE))

        self.nest.render(surface)

        for particle in self.particles[0]:
            particle.render(surface)

        for egg in self.eggs:
            egg.render(surface)

        for enemy in self.enemies:
            enemy.render(surface)

        self.active_player.render(surface)

        for particle in self.particles[1]:
            particle.render(surface)

        surface.blit(VIGNETTE, (0,0))



        for i in range(len(self.eggs)):
            surface.blit(EGG_SPRITESHEET[self.eggs[i].sprite_index if self.eggs[i].state!=4 else  5], (i*40+20, 20))

            if self.eggs[i].state==2 and math.sin(self.flash_tick*10)>0:
                surface.blit(EGG_SPRITESHEET[4], (i*40+20, 20))


        if self.game_over:
            surface.blit(self.restart_prompt, self.restart_prompt_rect)

            score_text=SCORE_FONT.render(str(self.game_score_render), 0, (255,255,255))
            surface.blit((score_text), score_text.get_rect(center=(SURFACE_WIDTH/2, SURFACE_HEIGHT/2-50))  )

        else:
            score_text=SCORE_FONT.render(str(self.game_score_render), 0, (255,255,255))
            surface.blit((score_text), score_text.get_rect(center=(590,40))  )

            surface.blit(CROSSHAIR_SPRITE, self.crosshair_rect)

