import pygame, random, math
from base_classes.scene import Scene
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_SIZE, TILE_SIZE, CHECK_COLOURS
from helper.utils import clamp

from game_elements.camera import Camera
from game_elements.player import Player
from game_elements.enemy import Enemy
from game_elements.egg import Egg
from game_elements.nest import Nest


from setup import EGG_SPRITESHEET


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



class Game(Scene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.map_data = [[ int((x%2)-(y%2)==0) for x in range(MAP_SIZE[0])] for y in range(MAP_SIZE[1]) ]

        self.map_rect=pygame.Rect(0,0,MAP_SIZE[0]*TILE_SIZE, MAP_SIZE[1]*TILE_SIZE)

        self.surface_size=(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.particles=[]
        self.eggs=[]
        self.enemies=[]

        self.nest_pos=self.map_rect.center


        self.active_cam=Camera(self.nest_pos, self.surface_size)
        self.active_player=Player( self.nest_pos, self.active_cam, self.particles)
        self.active_cam.follow_mode(self.active_player.pos, 4)

        self.nest=Nest(self.nest_pos, self.active_cam, self.particles)
        self.eggs.append(Egg(self.nest_pos, self.active_cam, self.particles, self.active_player.pos))

        # Spawning some enemies
        for i in range(10):
            rot=random.random()*math.pi*2
            dist=random.randint(self.nest_pos[0], self.nest_pos[0]+800)
            self.enemies.append(Enemy((math.sin(rot)*dist + self.nest_pos[0],math.cos(rot)*dist + self.nest_pos[1]), self.active_cam, self.particles, self.eggs))


    def handle_event(self, event):
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     print("Switching to MENU")
        #     self.game_manager.switch_scene(Menu)
        pass

    def update(self, dt):
        keys=pygame.key.get_pressed()
        mouse_pos=pygame.mouse.get_pos()

        self.active_player.update(keys, dt)
        self.active_cam.update(mouse_pos, dt)

        for i in range(len(self.particles)-1,-1,-1):
            particle=self.particles[i]
            particle.update((0,0), dt)

            if particle.is_dead():
                self.particles.pop(i)

        for enemy in self.enemies:
            enemy.update(dt)


    def render(self, surface):
        surface.fill((0,255,0))

        clip_start=[clamp(int(self.active_cam.render_pos[0]/TILE_SIZE)-1, 0, MAP_SIZE[0]),
                    clamp(int(self.active_cam.render_pos[1]//TILE_SIZE)-1, 0, MAP_SIZE[1])]
        clip_end=[clamp(int((self.active_cam.render_pos[0]+self.surface_size[0])//TILE_SIZE)+1, 0, MAP_SIZE[0]),
                  clamp(int((self.active_cam.render_pos[1]+self.surface_size[1])//TILE_SIZE)+1, 0, MAP_SIZE[1])]

        # Draw checkered ground
        for y in range(clip_start[1], clip_end[1]):
            for x in range(clip_start[0], clip_end[0]):
                pygame.draw.rect(surface, CHECK_COLOURS[self.map_data[y][x]],
                                            pygame.Rect(x*TILE_SIZE-self.active_cam.render_pos[0], y*TILE_SIZE-self.active_cam.render_pos[1], TILE_SIZE, TILE_SIZE))

        self.nest.render(surface)

        for egg in self.eggs:
            egg.render(surface)

        for enemy in self.enemies:
            enemy.render(surface)

        self.active_player.render(surface)

        for particle in self.particles:
            particle.render(surface)
