import pygame
from base_classes.gameobject import StatObj
from setup import NEST_SPRITE


class Nest(StatObj):
    def __init__(self, pos, camera_ref, particle_ref):
        super().__init__(pos, camera_ref, particle_ref)

        self.image_offset=(64, 32)


    def render(self, surface):
        super().render(surface, NEST_SPRITE)





