from abc import ABC, abstractmethod


class StatObj(ABC):
    def __init__(self, pos, camera_ref, particle_ref) -> None:
        '''An abstract GameObject'''
        self.pos=list(pos)
        self.camera_ref = camera_ref # remove?
        self.particle_ref = particle_ref
    

    def update(self, dt) -> None:
        '''Updates object values and perform calculations'''
        pass

    def render(self, surface, image, pos=None) -> None:
        if pos:
            surface.blit(image, (pos[0]-self.camera_ref.render_pos[0]-self.image_offset[0],         
                                                    pos[1]-self.camera_ref.render_pos[1] - self.image_offset[1]  )  )
        else:
            surface.blit(image, (self.pos[0]-self.camera_ref.render_pos[0]-self.image_offset[0],         
                                                    self.pos[1]-self.camera_ref.render_pos[1] - self.image_offset[1]  )  )


class AnimObj(ABC):
    def __init__(self, pos, camera_ref, particle_ref, state, facing=0, anim_rate=0.1) -> None:
        '''An abstract GameObject'''
        self.pos=list(pos)
        self.camera_ref = camera_ref # remove?
        self.particle_ref = particle_ref

        self.state=state
        self.facing=facing

        self.anim_tick=0
        self.anim_rate=anim_rate
    

    def update(self, dt) -> None:
        '''Updates object values and perform calculations'''
        pass

    def render(self, surface, animation) -> None:
        surface.blit(animation[self.state][ int(self.anim_tick/self.anim_rate)%(len(animation[self.state])-1)  ][self.facing]  ,
                     (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )


        
class Collectable(StatObj):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref, sprite, sprite_overlay, collection_radius=50):
        super().__init__(pos, camera_ref, particle_ref)
        
        self.player_pos_ref=player_pos_ref

        self.collection_radius=collection_radius
        self.calc_radius=self.collection_radius**2

        self.player_prox=False

        self.sprite_index=0
        highlight=sprite.copy()
        highlight.blit(sprite_overlay,(0,0))
        self.sprite=[sprite, highlight]


    def check_collection(self):
        return ((self.pos[0]-self.player_pos_ref[0])**2 + (self.pos[1]-self.player_pos_ref[1])**2)<self.calc_radius

    def render(self, surface, pos=None):
        super().render(surface, self.sprite[int(self.player_prox)], pos)
        


