from setup import BUNNY_ANIMATION, BOOMERANG_SPRITESHEET, PLAYER_WALK_SFX, THROW_SFX, BOOMERANG_SFX, DASH_SFX
from constants import PARTICLE_COLOURS, NORMALIZER_CONST, SURFACE_WIDTH, SURFACE_HEIGHT
from base_classes.gameobject import AnimObj, Collectable
from game_elements.particles import CircleParticle, DashParticle
import pygame, random, math

class Player(AnimObj):
    def __init__(self, pos, camera_ref, particle_ref, bounds):
        super().__init__(pos, camera_ref, particle_ref, "idle")

        self.offset=(32, 32)

        self.vel=[0,0]
        self.rot=0
        self.speed=200
        self.accel=3000
        self.friction_force=8

        self.weapon=Boomerang([pos[0]+100, pos[1]], camera_ref, particle_ref, self.pos)

        self.dash_speed=500
        self.dash_length=0.5
        self.dash_tick=0
        self.dash_freq=0.02
        self.dash_counter=0

        self.holding_egg=0

        self.walk_sfx_freq=0.2
        self.walk_sfx_tick=0

        self.bounds=( (bounds[0][0]+self.offset[0], bounds[1][0]-self.offset[0]), (bounds[0][1]+self.offset[1], bounds[1][1]-self.offset[1]) )


    def update(self, keys, pickup_key_event, mouse_state, mouse_pos, dt):

        if self.state!="game over":
            if self.state=="dash":
                self.dash_tick+=dt
                self.camera_ref.shake_amount=1.8
                if self.dash_tick/self.dash_freq>=self.dash_counter:
                    self.particle_ref[0].append(DashParticle(self.camera_ref, self.pos.copy(), 0.15, self.facing))
                    self.dash_counter+=1

                if self.dash_length<self.dash_tick:
                    self.state="idle"

            else:
                self.state="idle"
                if self.weapon.state!=0 and self.holding_egg==0 and keys[pygame.K_SPACE]:
                    dash_rot = math.atan2(( mouse_pos[0] - SURFACE_WIDTH/2 ),
                                ( mouse_pos[1] - SURFACE_HEIGHT/2))

                    self.camera_ref.shake_fade=8
                    self.vel, self.state, self.dash_tick, self.dash_counter = [math.sin(dash_rot)*self.dash_speed, math.cos(dash_rot)*self.dash_speed], "dash", 0, 0

                    pygame.mixer.Channel(4).play(DASH_SFX)

                else:
                    self.facing=int(mouse_pos[0]<SURFACE_WIDTH/2)
                    if keys[pygame.K_s]:self.vel[1], self.state = min(self.vel[1]+self.accel*dt, self.speed), "run"
                    if keys[pygame.K_w]:self.vel[1], self.state = max(self.vel[1]-self.accel*dt, -self.speed), "run"

                    if keys[pygame.K_d]:
                        self.vel[0], self.state = min(self.vel[0]+self.accel*dt, self.speed), "run"
                    if keys[pygame.K_a]:
                        self.vel[0], self.state = max(self.vel[0]-self.accel*dt, -self.speed), "run"

                if self.state=="run":

                    if self.walk_sfx_tick>self.walk_sfx_freq:
                        pygame.mixer.Channel(0).play(PLAYER_WALK_SFX)
                        self.walk_sfx_tick=0
                    else:
                        self.walk_sfx_tick+=dt


                self.vel[0]-=self.vel[0]*self.friction_force*dt
                self.vel[1]-=self.vel[1]*self.friction_force*dt


            self.pos[0]= max(min(self.pos[0]+self.vel[0]*dt, self.bounds[0][1]), self.bounds[0][0])
            self.pos[1]= max(min(self.pos[1]+self.vel[1]*dt, self.bounds[1][1]), self.bounds[1][0])


            self.weapon.update(pickup_key_event, mouse_state, mouse_pos, dt)


        self.holding_anim=self.holding_egg
        if self.weapon.state==0 and self.state!="dash": self.holding_anim=1
        if self.state=="game over": self.holding_anim=0


        self.anim_tick+=dt





    def render(self, surface):
        if self.weapon.state==2:
            self.weapon.render(surface)
            surface.blit(BUNNY_ANIMATION[self.state][self.holding_anim][ int(self.anim_tick/self.anim_rate)%(len(BUNNY_ANIMATION[self.state][self.holding_anim])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )

        else:

            surface.blit(BUNNY_ANIMATION[self.state][self.holding_anim][ int(self.anim_tick/self.anim_rate)%(len(BUNNY_ANIMATION[self.state][self.holding_anim])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )
            self.weapon.render(surface)





class Boomerang(Collectable):
    def __init__(self, pos, camera_ref, particle_ref, player_pos_ref):
        super().__init__(pos, camera_ref, particle_ref, player_pos_ref, BOOMERANG_SPRITESHEET[0], BOOMERANG_SPRITESHEET[4], collection_radius=50)
        self.image_offset=(16,16)

        self.state=2
        #state: 0=held 1=thrown 2=dropped

        self.vel=[0,0]
        self.throw_speed=600
        self.rot=0


        self.spin_sfx_freq=0.3
        self.spin_sfx_tick=0




    def update(self, pickup_key_event, mouse_state, mouse_pos, dt):
        self.player_prox=False

        if self.state==0:
            self.pos=[self.player_pos_ref[0]-10, self.player_pos_ref[1]-35]
            if mouse_state[0]:
                self.state=1
                self.pos=[self.pos[0], self.pos[1]]


                self.throw_life=2
                self.throw_tick=0

                throw_angle=math.atan2(( mouse_pos[0] - (SURFACE_WIDTH/2-10) ),
                               ( mouse_pos[1] - (SURFACE_HEIGHT/2-35)))

                self.vel=[math.sin(throw_angle)*self.throw_speed, math.cos(throw_angle)*self.throw_speed]
                self.return_force=(-self.vel[0], -self.vel[1])

                pygame.mixer.Channel(2).play(THROW_SFX)
                self.spin_sfx_tick=self.spin_sfx_freq

        else:
            self.player_prox=self.check_collection()

            if self.state==1:
                self.vel[0]+=self.return_force[0]*dt
                self.vel[1]+=self.return_force[1]*dt

                self.pos[0]+=self.vel[0]*dt
                self.pos[1]+=self.vel[1]*dt

                self.rot+=dt*600


                if self.throw_life<self.throw_tick:
                    self.state=2

                self.throw_tick+=dt

                for i in range(round(100*dt)):
                    self.particle_ref[1].append(CircleParticle(self.camera_ref, self.pos.copy(), [random.randint(-400,400)+self.vel[0]*-2, random.randint(-400,400)+self.vel[1]*-2], PARTICLE_COLOURS[random.randint(0,len(PARTICLE_COLOURS)-1)], random.randint(1,3), 0.5)  )


                #Sound
                if self.spin_sfx_tick>self.spin_sfx_freq:
                    pygame.mixer.Channel(3).play(BOOMERANG_SFX)
                    self.spin_sfx_tick=0
                else:
                    self.spin_sfx_tick+=dt



            if self.player_prox and pickup_key_event:
                self.state=0






    def render(self, surface):
        if self.state==1:
            rot_sprite=pygame.transform.rotate(self.sprite[int(self.player_prox)], self.rot)
            surface.blit(rot_sprite, rot_sprite.get_rect(center = (self.pos[0]-self.camera_ref.render_pos[0],
                                                                self.pos[1]-self.camera_ref.render_pos[1])  ) )
        else:
             super().render(surface)




