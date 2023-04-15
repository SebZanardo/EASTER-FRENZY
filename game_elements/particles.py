import pygame
from setup import BUNNY_DASH_SPRITES


class BaseParticle:
    def __init__(self, camera_ref, pos, vel, friction, life):
        self.camera_ref=camera_ref
        self.pos=list(pos)
        self.vel=list(vel)

        self.life=life
        self.age=0

        self.friction=friction

        self.is_dead=False


    def update(self, dt):
        self.vel[0]-=self.vel[0]*self.friction*dt
        self.vel[1]-=self.vel[1]*self.friction*dt

        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt

        self.age+=dt

        self.is_dead=self.age>self.life        

    
class CircleParticle(BaseParticle):
    def __init__(self, camera_ref, pos, vel, colour, radius, life):
        super().__init__(camera_ref, pos, vel, 10, life)
        self.colour=colour
        self.radius=radius


    def render(self, surface):
        pygame.draw.circle(surface, self.colour, [self.pos[0]-self.camera_ref.render_pos[0],   self.pos[1]-self.camera_ref.render_pos[1]], self.radius)



class ImageParticle(BaseParticle):
    def __init__(self, camera_ref, pos, vel, friction, life, sprite):
        super().__init__(camera_ref, pos, vel, friction, life)

        self.sprite=sprite
        self.size=sprite.get_size()
        self.offset=(self.size[0]/2, self.size[1]/2)

    def render(self, surface):
        surface.blit(self.sprite, (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0],   self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]))


class DashParticle(BaseParticle):
    def __init__(self, camera_ref, pos, life, facing):
        super().__init__(camera_ref, pos, [0,0], 0, life)
        self.offset=(32, 32)
        self.facing=facing

        self.sprite_period=life/6

    def render(self, surface):
        surface.blit(BUNNY_DASH_SPRITES[min(int(self.age/self.sprite_period), 2)   ][self.facing], (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0],   self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]))



class ScoreParticle(ImageParticle):
    def __init__(self, camera_ref, pos, life, text_sprite):
        super().__init__(camera_ref, pos, (0,-200), 5, life, text_sprite)

        self.fade_rate=350/life
        self.fade_tick=0

    def update(self, dt):
        super().update(dt)
        self.sprite.set_alpha( min(max(350-self.fade_rate*self.fade_tick, 0), 255)  )


        self.fade_tick+=dt

