from base_classes.gameobject import StatObj
import pygame

from setup import NEST_SPRITE


class Nest(StatObj):
    def __init__(self, pos, camera_ref, particle_ref):
        super().__init__(pos, camera_ref, particle_ref)

        self.sprite_size=NEST_SPRITE.get_size()
        self.image_offset=(self.sprite_size[0]//2, self.sprite_size[1]//2)


    def render(self, surface):
        super().render(surface, NEST_SPRITE)





