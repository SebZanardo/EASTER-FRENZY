from abc import ABC, abstractmethod


class StatObj(ABC):
    def __init__(self, pos, camera_ref, particle_ref) -> None:
        '''An abstract GameObject'''
        self.pos=list(pos)
        self.camera_ref = camera_ref
        self.particle_ref = particle_ref


    def update(self, dt) -> None:
        '''Updates object values and perform calculations'''
        pass

    def render(self, surface, image) -> None:
        surface.blit(image, (self.pos[0]-self.camera_ref.render_pos[0]-self.image_offset[0], self.pos[1]-self.camera_ref.render_pos[1] - self.image_offset[1]))


class AnimObj(ABC):
    def __init__(self, pos, camera_ref, particle_ref, state, facing=0, anim_rate=0.1) -> None:
        '''An abstract GameObject'''
        self.pos=list(pos)
        self.camera_ref = camera_ref
        self.particle_ref = particle_ref

        self.state=state
        self.facing=facing

        self.anim_tick=0
        self.anim_rate=anim_rate


    def update(self, dt) -> None:
        '''Updates object values and perform calculations'''
        pass

    def render(self, surface, animation) -> None:
        surface.blit(animation[self.state][int(self.anim_tick/self.anim_rate)%(len(animation[self.state])-1)][self.facing],
                     (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )




