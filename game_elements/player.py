from setup import BUNNY_ANIMATION, BOOMERANG_SPRITESHEET
from constants import PARTICLE_COLOURS, NORMALIZER_CONST, SURFACE_WIDTH, SURFACE_HEIGHT
from gameobject import AnimObj, Collectable
from game_elements.particles import CircleParticle, DashParticle
import pygame, random, math

class Player(AnimObj):
    def __init__(self, pos, camera_ref, particle_ref):
        super().__init__(pos, camera_ref, particle_ref, "idle")

        self.offset=(32, 32)

        self.vel=[0,0]
        self.rot=0
        self.speed=200
        self.accel=3000
        self.friction_force=8

        self.weapon=Boomerang(pos, camera_ref, particle_ref, self.pos)

        self.dash_speed=400
        self.dash_length=0.5
        self.dash_tick=0
        self.dash_freq=0.02
        self.dash_counter=0



    def update(self, keys, mouse_state, mouse_pos, dt):

        if self.state=="dash":
            self.dash_tick+=dt
            if self.dash_tick/self.dash_freq>=self.dash_counter:
                self.particle_ref.append(DashParticle(self.camera_ref, self.pos.copy(), 0.15, self.facing))
                self.dash_counter+=1

            if self.dash_length<self.dash_tick:
                self.state="idle"

        else:
            self.state="idle"
            if self.weapon.state!=0 and keys[pygame.K_SPACE]:
                dash_rot = math.atan2(( mouse_pos[0] - SURFACE_WIDTH/2 ),
                               ( mouse_pos[1] - SURFACE_HEIGHT/2))
                self.vel, self.state, self.dash_tick, self.dash_counter = [math.sin(dash_rot)*self.dash_speed, math.cos(dash_rot)*self.dash_speed], "dash", 0, 0
            else:
                self.facing=int(mouse_pos[0]<SURFACE_WIDTH/2)
                if keys[pygame.K_s]:self.vel[1], self.state = min(self.vel[1]+self.accel*dt, self.speed), "run"
                if keys[pygame.K_w]:self.vel[1], self.state = max(self.vel[1]-self.accel*dt, -self.speed), "run"

                if keys[pygame.K_d]:self.vel[0], self.state = min(self.vel[0]+self.accel*dt, self.speed), "run"
                if keys[pygame.K_a]:self.vel[0], self.state = max(self.vel[0]-self.accel*dt, -self.speed), "run"


            self.vel[0]-=self.vel[0]*self.friction_force*dt
            self.vel[1]-=self.vel[1]*self.friction_force*dt


        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt

        self.weapon.update(keys, mouse_state, mouse_pos, dt)


        if False:
            for i in range(15):
                angle=random.random()/2+self.rot
                self.particle_ref.append(Particle(self.camera_ref, self.pos.copy(), [math.sin(angle)*random.randint(400,1500), math.cos(angle)*random.randint(400,1500)], PARTICLE_COLOURS[random.randint(0,len(PARTICLE_COLOURS)-1)], random.randint(2,5), 4  ))

        self.anim_tick+=dt


    def render(self, surface):
        if self.weapon.state==2:
            self.weapon.render(surface)
            surface.blit(BUNNY_ANIMATION[self.state][ int(self.anim_tick/self.anim_rate)%(len(BUNNY_ANIMATION[self.state])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )

        else:
            surface.blit(BUNNY_ANIMATION[self.state][ int(self.anim_tick/self.anim_rate)%(len(BUNNY_ANIMATION[self.state])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )
            self.weapon.render(surface)





class Boomerang(Collectable):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref):
        super().__init__(pos, camera_ref, particle_ref, player_pos_ref, BOOMERANG_SPRITESHEET[0], BOOMERANG_SPRITESHEET[4], collection_radius=50)
        self.image_offset=(16,16)

        self.state=0
        #state: 0=held 1=thrown 2=dropped

        self.vel=[0,0]
        self.throw_speed=600
        self.rot=0


    def update(self, keys, mouse_state, mouse_pos, dt):
        self.player_prox=False

        if self.state==0:
            self.pos=self.player_pos_ref
            if mouse_state[0]:
                self.state=1
                self.pos=self.player_pos_ref.copy()

                self.throw_life=2
                self.throw_tick=0

                throw_angle=math.atan2(( mouse_pos[0] - SURFACE_WIDTH/2 ),
                               ( mouse_pos[1] - SURFACE_HEIGHT/2))

                self.vel=[math.sin(throw_angle)*self.throw_speed, math.cos(throw_angle)*self.throw_speed]
                self.return_force=(-self.vel[0], -self.vel[1])

        else:
            if self.state==1:
                self.vel[0]+=self.return_force[0]*dt
                self.vel[1]+=self.return_force[1]*dt

                self.pos[0]+=self.vel[0]*dt
                self.pos[1]+=self.vel[1]*dt

                self.rot+=dt*400


                if self.throw_life<self.throw_tick:
                    self.state=2

                self.throw_tick+=dt

                for i in range(3):
                    self.particle_ref.append(CircleParticle(self.camera_ref, self.pos.copy(), [random.randint(-400,400)+self.vel[0]*-2, random.randint(-400,400)+self.vel[1]*-2], PARTICLE_COLOURS[random.randint(0,len(PARTICLE_COLOURS)-1)], random.randint(1,3), 0.5)  )


            self.player_prox=self.check_collection()
            if self.player_prox and keys[pygame.K_f]:
                self.state=0






    def render(self, surface):
        if self.state==1:
            rot_sprite=pygame.transform.rotate(self.sprite[0], self.rot)
            surface.blit(rot_sprite, rot_sprite.get_rect(center = (self.pos[0]-self.camera_ref.render_pos[0],
                                                                self.pos[1]-self.camera_ref.render_pos[1])  ) )
        else:
             super().render(surface)




