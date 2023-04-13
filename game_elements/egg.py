from base_classes.gameobject import StatObj
from setup import EGG_SPRITESHEET

class Collectable(StatObj):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref):
        super().__init__(pos, camera_ref, particle_ref)
        self.image_offset=(20,20)

        self.player_pos_ref=player_pos_ref

        self.collection_radius=50
        self.calc_radius=self.collection_radius**2

        self.player_prox=False


    def check_collection(self):
        return ((self.pos[0]-self.player_pos_ref[0])**2 + (self.pos[1]-self.player_pos_ref[1])**2)<self.calc_radius

    def render(self, surface):
        super().render(surface, self.sprite[int(self.player_prox)])



class Egg(Collectable):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref):
        super().__init__(pos, camera_ref, particle_ref, player_pos_ref)
        self.state=0

        #state: 0="nested" 1="dropped" 2="captured" 3="held"

        self.sprite_index=0
        highlight=EGG_SPRITESHEET[self.sprite_index].copy()
        highlight.blit(EGG_SPRITESHEET[4],(0,0))
        self.sprite=[EGG_SPRITESHEET[self.sprite_index], highlight]


    def update(self, dt):
        if self.state==0:
            pass
        elif self.state==1:
            self.move_period+=dt
            self.player_prox=self.check_collection()
        elif self.state==2:
            pass
        else:
            self.pos=self.player_pos_ref




