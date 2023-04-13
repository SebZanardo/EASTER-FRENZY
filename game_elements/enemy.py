import pygame, math
from base_classes.gameobject import AnimObj
from setup import ENEMY_ANIMATION

class Enemy(AnimObj):
    def __init__(self, pos, camera_ref, particle_ref, eggs_ref):
        super().__init__(pos, camera_ref, particle_ref, "run")
        self.offset=(32,32)
        self.eggs_ref=eggs_ref

        self.origin=pos
        self.target_egg_index=self.find_closest_egg()
        self.egg_pos=self.eggs_ref[self.target_egg_index].pos

        rot=math.atan2(  (self.pos[1]-self.egg_pos[1]), (self.pos[0]-self.egg_pos[0]) )
        self.rotUV=[-math.cos(rot), -math.sin(rot)]
        if self.rotUV[0]<0: self.facing=1

        self.dist_thresh=20**2
        self.holding=False

        self.dynamic=True


    def find_closest_egg(self):
        dist=[ (self.pos[0]-egg.pos[0])**2 + (self.pos[1]-egg.pos[1])**2   for egg in self.eggs_ref]
        exist=False
        cur_min=9999999
        for i in range(len(self.eggs_ref)):
            egg=self.eggs_ref[i]
            if egg.state<2:
                dist=(self.pos[0]-egg.pos[0])**2 + (self.pos[1]-egg.pos[1])**2
                if dist<cur_min:
                    cur_min, index, exist = dist, i, True

        return  i if exist else False


    def update(self,dt):
        if self.dynamic:
            self.anim_tick+=dt
            self.pos[0]+=self.rotUV[0]
            self.pos[1]+=self.rotUV[1]


        if not self.holding:
            if self.eggs_ref[self.target_egg_index].state>1:
                closest=self.find_closest_egg()
                if closest==False:
                    self.dynamic=False
                else:
                    self.target_egg_index=self.find_closest_egg()
                    self.egg_pos=self.eggs_ref[self.target_egg_index].pos

            if self.dynamic and (self.pos[0]-self.egg_pos[0])**2 + (self.pos[1]-self.egg_pos[1])**2 <self.dist_thresh :
                self.rotUV[0]*=-1
                self.rotUV[1]*=-1
                self.facing=int(not self.facing)
                self.holding=True
                self.eggs_ref[self.target_egg_index].pos=self.pos
                self.eggs_ref[self.target_egg_index].state=2




    def render(self, surface):
        surface.blit(ENEMY_ANIMATION[self.state][ int(self.anim_tick/self.anim_rate)%(len(ENEMY_ANIMATION[self.state])-1)  ][self.facing]  ,
                     (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )


