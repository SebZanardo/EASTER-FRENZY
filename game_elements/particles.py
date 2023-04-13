import pygame

class Particle:
    def __init__(self, camera_ref, pos, vel, colour, size, life):
        self.camera_ref=camera_ref
        
        self.pos=list(pos)
        self.vel=list(vel)

        self.life=life
        self.age=0

        self.colour=colour
        self.size=size
        self.dead=False

    def update(self,force,dt):
        self.vel[0]= (force[0]*dt+self.vel[0])*0.9
        self.vel[1]= (force[1]*dt+self.vel[1])*0.9

        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt

        self.age+=dt

    def is_dead(self):
        return self.age>self.life


    def render(self, surface):
        pygame.draw.circle(surface, self.colour, [self.pos[0]-self.camera_ref.render_pos[0],   self.pos[1]-self.camera_ref.render_pos[1]], self.size)
