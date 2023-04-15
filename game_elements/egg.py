from base_classes.gameobject import Collectable
from setup import EGG_SPRITESHEET, SHADOW_SPRITE, STAR_PARTICLE_SPRITE, SCORE_PARTICLE_SPRITES
from game_elements.particles import ImageParticle, ScoreParticle
import pygame, math, random


class Egg(Collectable):
    def __init__(self, pos, camera_ref, particle_ref, player_ref, boomerang_ref, sprite_index, nest_pos):

        super().__init__(pos, camera_ref, particle_ref, player_ref.pos, EGG_SPRITESHEET[sprite_index], EGG_SPRITESHEET[4], collection_radius=50)
        self.state=0
        self.image_offset=(20,20)
        self.move_period=0

        self.boomerang_ref=boomerang_ref
        self.player_ref=player_ref

        self.origin_pos=pos.copy()

        self.sprite_index=sprite_index

        self.nest_pos=nest_pos


        #state: 0="nested" 1="dropped" 2="captured" 3="held" 4="gone"





    def update(self, pickup_key_event, dt):
        self.player_prox=False
        self.score_return=0

        if self.state==0:
            pass
        elif self.state==1:
            self.move_period+=dt
            self.player_prox=self.check_collection()

            if self.player_prox and pickup_key_event and self.player_ref.state!="dash" and self.player_ref.holding_egg==0:
                self.state=3

                if self.player_ref.holding_egg==0:
                    if self.boomerang_ref.state==0:
                        self.boomerang_ref.state=2
                        self.boomerang_ref.pos=self.boomerang_ref.pos.copy()
                    self.player_ref.holding_egg=1



        elif self.state==2:
            pass

        elif self.state==3:
            self.pos=[self.player_pos_ref[0], self.player_pos_ref[1]-40 ]

            if ((self.pos[0]-self.nest_pos[0])**2 + (self.pos[1]+35-self.nest_pos[1])**2)<self.calc_radius:
                self.state=0
                self.pos=self.origin_pos.copy()
                self.player_ref.holding_egg=0

                for i in range(20):
                    self.particle_ref[1].append(ImageParticle(self.camera_ref, self.pos, [random.randint(-200,200), random.randint(-300,0)], 4, 0.5, STAR_PARTICLE_SPRITE ))

                self.particle_ref[1].append(ScoreParticle(self.camera_ref, self.pos.copy(), 1, SCORE_PARTICLE_SPRITES[1]))
                self.score_return=20

            elif pickup_key_event:
                self.state=1
                self.player_ref.holding_egg=0







    def render(self, surface):
        if self.state!=4:
            if self.state==1:
                surface.blit(SHADOW_SPRITE, (self.pos[0]-self.camera_ref.render_pos[0]-16,
                                                self.pos[1]-self.camera_ref.render_pos[1]-16  ))

            super().render(surface, (self.pos[0], self.pos[1]-math.sin(self.move_period*5)*8-12 ) if self.state==1 else None )





