import pygame
from helper.utils import point_rect_col

class Button:
    def __init__(self, pos, image, scale_factor):
        self.pos=pos

        temp_rect=image.get_rect(center=pos)

        self.image=(image, pygame.transform.scale(image, (temp_rect.width*scale_factor, temp_rect.height*scale_factor)))
        self.rect=(temp_rect, self.image[1].get_rect(center=pos))

        self.hover=False

    def update(self, mouse_pos):
        self.hover = int(self.rect[self.hover].collidepoint(mouse_pos))

    def render(self, surface):
        surface.blit(self.image[self.hover], self.rect[self.hover])
