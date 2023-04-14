from gameobject import Collectable 
from setup import EGG_SPRITESHEET, SHADOW_SPRITE
import pygame, math


class Egg(Collectable):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref):
        self.sprite_index=0

        super().__init__(pos, camera_ref, particle_ref, player_pos_ref, EGG_SPRITESHEET[self.sprite_index], EGG_SPRITESHEET[4], collection_radius=50)
        self.state=0
        self.image_offset=(20,20)
        self.move_period=0
        
        #state: 0="nested" 1="dropped" 2="captured" 3="held"


        


    def update(self, dt):
        self.player_prox=False


        if self.state==0:
            pass
        elif self.state==1:
            self.move_period+=dt
            self.player_prox=self.check_collection()
            
        elif self.state==2: 
            pass
        else:
            self.pos=self.player_pos_ref

    
    def render(self, surface):
        if self.state==1:
            surface.blit(SHADOW_SPRITE, (self.pos[0]-self.camera_ref.render_pos[0]-16,         
                                            self.pos[1]-self.camera_ref.render_pos[1]-16  ))

        super().render(surface, (self.pos[0], self.pos[1]-math.sin(self.move_period*5)*8-12 ) if self.state==1 else None )

   

        
    
