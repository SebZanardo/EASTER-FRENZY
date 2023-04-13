import pygame
import random
import math

from setup import BUNNY_ANIMATION
from constants import PARTICLE_COLOURS, NORMALIZER_CONST
from base_classes.gameobject import AnimObj
from game_elements.particles import Particle


class Player(AnimObj):
    def __init__(self, pos, camera_ref, particle_ref):
        super().__init__(pos, camera_ref, particle_ref, "idle")

        self.offset=(32, 32)

        self.vel=[0,0]
        self.rot=0
        self.speed=200
        self.accel=3000
        self.friction_force=8

    def update(self, keys, dt):

        self.state="idle"

        if keys[pygame.K_s]:self.vel[1], self.state = min(self.vel[1]+self.accel*dt, self.speed), "run"
        if keys[pygame.K_w]:self.vel[1], self.state = max(self.vel[1]-self.accel*dt, -self.speed), "run"

        if keys[pygame.K_d]:self.vel[0], self.state, self.facing = min(self.vel[0]+self.accel*dt, self.speed), "run", 0
        elif keys[pygame.K_a]:self.vel[0], self.state, self.facing = max(self.vel[0]-self.accel*dt, -self.speed), "run", 1

        self.vel[0]-=self.vel[0]*self.friction_force*dt
        self.vel[1]-=self.vel[1]*self.friction_force*dt

        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt

        self.rot+=dt

        if True:
            for i in range(15):
                angle=random.random()/2+self.rot
                self.particle_ref.append(Particle(self.camera_ref, self.pos.copy(), [math.sin(angle)*random.randint(400,1500), math.cos(angle)*random.randint(400,1500)], PARTICLE_COLOURS[random.randint(0,len(PARTICLE_COLOURS)-1)], random.randint(2,5), 4  ))

        self.anim_tick+=dt


    def render(self, surface):
        surface.blit(BUNNY_ANIMATION[self.state][ int(self.anim_tick/self.anim_rate)%(len(BUNNY_ANIMATION[self.state])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )

