import pygame, math, random
from gameobject import AnimObj
from setup import ENEMY_ANIMATION, BLOOD_PARTICLES
from constants import PARTICLE_COLOURS, BLOOD_COLOURS, SPIDER_COLOURS
from utils import point_rect_col
from game_elements.particles import CircleParticle, ImageParticle
from enum import Enum, auto

class States(Enum):
    SEARCHING = "run"
    CARRYING = "carry"
    SCATTER = "scatter"
    DYING = "hit"

class Enemy(AnimObj):
    def __init__(self, pos, camera_ref, particle_ref, eggs_ref, weapon_ref):
        super().__init__(pos, camera_ref, particle_ref, States.SEARCHING)
        self.offset=(32,32)
        self.collider_size=(64,64)

        self.eggs_ref=eggs_ref
        self.weapon_ref=weapon_ref

        self.origin=pos

        self.target_egg_index =self.find_closest_egg()

        self.target_egg_pos =self.eggs_ref[self.target_egg_index].pos
        self.random_pos = None

        rot = math.atan2(  (self.pos[1]-self.target_egg_pos[1]), (self.pos[0]-self.target_egg_pos[0]) )
        self.rotUV = [-math.cos(rot), -math.sin(rot)]
        if self.rotUV[0]<0:
            self.facing=1

        self.dist_thresh=20**2

        self.is_dead = False
        self.dying_timer = 0.2
        self.speed = 120
        self.carry_speed = 60


    def find_closest_egg(self):
        dist=[(self.pos[0]-egg.pos[0])**2 + (self.pos[1]-egg.pos[1])**2 for egg in self.eggs_ref]

        cur_min, index = None, None
        for i in range(0, len(dist)):
            if (cur_min==None or dist[i]<cur_min) and self.eggs_ref[i].state<2:
                cur_min, index = dist[i], i

        return index

    def find_random_pos(self):
        return (self.pos[0] + (random.randint(100,200) * random.choice([-1,1])),
                self.pos[1] + (random.randint(100,200) * random.choice([-1,1])))


    def update(self,dt):
        # Weapon thrown
        if self.weapon_ref.state==1 and not self.state == States.DYING:
            if point_rect_col(self.weapon_ref.pos, (self.pos[0]-self.offset[0], self.pos[1]-self.offset[1], * self.collider_size)):
                # Drop Egg if carrying
                if self.state == States.CARRYING:
                    self.eggs_ref[self.target_egg_index].state=1
                    self.eggs_ref[self.target_egg_index].pos=self.pos.copy()
                    self.eggs_ref[self.target_egg_index].move_period=0

                # Blood Particles
                angular_vel=self.weapon_ref.vel
                for i in range(20):
                    angle=random.random()*math.pi*2
                    self.particle_ref.append(ImageParticle(self.camera_ref, self.pos.copy(), [random.random()*angular_vel[0]*3, random.random()*angular_vel[1]*3], random.randint(3,5), BLOOD_PARTICLES[random.randint(0,len(BLOOD_PARTICLES)-1)]))
                    #self.particle_ref.append(CircleParticle(self.camera_ref, self.pos.copy(), [random.randint(-1000,1000)+angular_vel[0], random.randint(-700,700)+angular_vel[1]], SPIDER_COLOURS[random.randint(0,len(SPIDER_COLOURS)-1)], random.randint(1,2), 0.2))

                self.state = States.DYING
                return

        # Spider movement
        if not self.state == States.DYING:
            self.anim_tick+=dt
            if self.state == States.CARRYING:
                self.pos[0]+=self.rotUV[0]*dt*self.carry_speed
                self.pos[1]+=self.rotUV[1]*dt*self.carry_speed
            elif self.state == States.SEARCHING or self.state == States.SCATTER:
                self.pos[0]+=self.rotUV[0]*dt*self.speed
                self.pos[1]+=self.rotUV[1]*dt*self.speed

        if not self.state == States.DYING and not self.state == States.CARRYING:
            closest = self.find_closest_egg()

            # Scatter if no eggs on ground
            if closest == None:

                if self.state != States.SCATTER:
                    self.state = States.SCATTER
                    self.random_pos = self.find_random_pos()
                    rot= math.atan2((self.pos[1]-self.random_pos[1]), (self.pos[0]-self.random_pos[0]) )
                    self.rotUV=[-math.cos(rot), -math.sin(rot)]
                    self.facing = int(self.rotUV[0]<0)

            # Head to egg
            else:
                self.state = States.SEARCHING

                self.target_egg_index= closest
                self.target_egg_pos= self.eggs_ref[self.target_egg_index].pos

                rot= math.atan2((self.pos[1]-self.target_egg_pos[1]), (self.pos[0]-self.target_egg_pos[0]) )
                self.rotUV=[-math.cos(rot), -math.sin(rot)]
                self.facing = int(self.rotUV[0]<0)


            if self.state == States.SEARCHING and ((self.pos[0]-self.target_egg_pos[0])**2 + (self.pos[1]-self.target_egg_pos[1])**2) <self.dist_thresh :
                # Picks up egg
                self.state = States.CARRYING
                self.rotUV[0] *= -1
                self.rotUV[1] *= -1
                self.facing = int(not self.facing)
                self.eggs_ref[self.target_egg_index].pos = self.pos
                self.eggs_ref[self.target_egg_index].state = 2

            if self.state == States.SCATTER and ((self.pos[0]-self.random_pos[0])**2 + (self.pos[1]-self.random_pos[1])**2) <self.dist_thresh:
                # Set new random pos
                self.random_pos = self.find_random_pos()
                rot= math.atan2((self.pos[1]-self.random_pos[1]), (self.pos[0]-self.random_pos[0]) )
                self.rotUV=[-math.cos(rot), -math.sin(rot)]
                self.facing = int(self.rotUV[0]<0)

        if self.state == States.DYING:
            self.dying_timer -= dt
            if self.dying_timer <= 0:
                self.is_dead = True

    def render(self, surface):
        surface.blit(ENEMY_ANIMATION[self.state.value][ int(self.anim_tick/self.anim_rate)%(len(ENEMY_ANIMATION[self.state.value])-1)  ][self.facing]  ,
                     (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )

