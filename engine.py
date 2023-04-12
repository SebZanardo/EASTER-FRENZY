import random
import math
import pygame
from constants import PARTICLE_COLOURS, CHECK_COLOURS

def clamp(v, b_thresh, t_thresh):
    return max(min(v, t_thresh), b_thresh)


def load_tiles(path, anim_length, tile_size, upscale_size, flip=False):
    temp_image=pygame.image.load(path).convert_alpha()
    tile_size=tile_size
    upscale_size=upscale_size

    tiles=[]
    for i in range(anim_length):
        tile=pygame.Surface(tile_size, pygame.SRCALPHA)
        tile.blit(temp_image, (0,0), (i*tile_size[0],0,*tile_size))
        tile=pygame.transform.scale(tile, upscale_size).convert_alpha()
        if flip:tiles.append([tile, pygame.transform.flip(tile, 1,0)])
        else:tiles.append(tile)

    return tiles




class camera:
    def __init__(self, pos, camera_size):
        self.pos=pos
        self.camera_size=camera_size
        self.render_offset=[camera_size[0]//2, camera_size[1]//2]

        self.mode=None
        self.speed=None

    def follow_mode(self, target, speed=1):
        self.mode="follow"
        self.follow_target=target
        self.speed=speed
        self.pos_raw=self.pos


    def update(self, keys, mouse_pos, mouse_state, dt):
        if self.mode:
            if self.mode=="follow":
                self.pos_raw=[ self.pos_raw[0]-(self.pos_raw[0]-self.follow_target[0])*dt*self.speed, self.pos_raw[1]-(self.pos_raw[1]-self.follow_target[1])*dt*self.speed  ]
                self.pos=[self.pos_raw[0]+(mouse_pos[0]-self.render_offset[0])/6,
                            self.pos_raw[1]+(mouse_pos[1]-self.render_offset[1])/6]

        self.render_pos=[self.pos[0]-self.render_offset[0], self.pos[1]-self.render_offset[1]]








class collectable:
    def __init__(self, surface_ref, camera_ref, player_pos_ref, image, pos):
        self.surface_ref=surface_ref
        self.camera_ref=camera_ref
        self.player_pos_ref=player_pos_ref

        self.pos=pos

        self.collection_radius=50
        self.calc_radius=self.collection_radius**2

        self.image=image
        self.image_offset=image.get_rect().center

    def check_collection(self):
        return ((self.pos[0]-self.player_pos_ref[0])**2 + (self.pos[1]-self.player_pos_ref[1])**2)<self.calc_radius

    def render(self):
        self.surface_ref.blit(self.image, (self.pos[0]-self.camera_ref.render_pos[0]-self.image_offset[0],         self.pos[1]-self.camera_ref.render_pos[1]  -self.image_offset[1]  )  )



class egg(collectable):
    def __init__(self, surface_ref, camera_ref, player_pos_ref, image, pos):
        super().__init__(surface_ref, camera_ref, player_pos_ref, image, pos)
        #self.move_period=random.random()
        self.dropped=False

    def update(self, dt):
        if self.dropped :
            self.move_period+=dt
            return self.check_collection()
        else:
            pass

        return False








class particle:
    def __init__(self, surface_ref, camera_ref, pos, vel, colour, size, life):
        self.surface_ref=surface_ref
        self.camera_ref=camera_ref

        self.pos=list(pos)
        self.vel=list(vel)

        self.life=life
        self.age=0

        self.colour=colour
        self.size=size

    def update(self,force,dt):
        self.vel[0]= (force[0]*dt+self.vel[0])*0.9
        self.vel[1]= (force[1]*dt+self.vel[1])*0.9



        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt

        self.age+=dt
        if self.age>self.life:return True
        return False

    def render(self):
        pygame.draw.circle(self.surface_ref, self.colour, [self.pos[0]-self.camera_ref.render_pos[0],   self.pos[1]-self.camera_ref.render_pos[1]], self.size)



class enemy:
    def __init__(self, surface_ref, camera_ref, particle_ref, eggs_ref, pos):
        self.surface_ref=surface_ref
        self.camera_ref=camera_ref
        self.particle_ref=particle_ref

        self.eggs_ref=eggs_ref

        self.pos=list(pos)
        self.origin=pos

        self.target_egg=self.find_closest_egg()
        self.speed = 200


        rot=math.atan2(  (self.pos[1]-self.target_egg[1]), (self.pos[0]-self.target_egg[0]) )
        self.rotUV=[-math.cos(rot), -math.sin(rot)]

        self.dist_thresh=20**2
        self.holding=False


    def find_closest_egg(self):
        dist=[ (self.pos[0]-egg.pos[0])**2 + (self.pos[1]-egg.pos[1])**2   for egg in self.eggs_ref]
        return  self.eggs_ref[dist.index(min(dist))].pos




    def update(self, dt):

        self.pos[0]+=self.rotUV[0] * self.speed * dt
        self.pos[1]+=self.rotUV[1] * self.speed * dt


        if not self.holding and (self.pos[0]-self.target_egg[0])**2 + (self.pos[1]-self.target_egg[1])**2 <self.dist_thresh :
            self.rotUV[0]*=-1
            self.rotUV[1]*=-1



    def render(self):
        pygame.draw.circle(self.surface_ref, (0,255,0), (self.pos[0]-self.camera_ref.render_pos[0],  self.pos[1]-self.camera_ref.render_pos[1] ), 20    )





class player:
    def __init__(self, surface_ref, camera_ref, particle_ref, pos):
        self.surface_ref=surface_ref
        self.camera_ref=camera_ref
        self.particle_ref=particle_ref

        self.pos=list(pos)
        self.vel=[0,0]
        self.rot=0
        self.speed=200
        self.accel=3000
        self.friction_force=8

        raw_animation_seq=load_tiles("assets/player-Sheet.png", 10, (64,64), (64,64), True)
        self.animation_data={"idle":raw_animation_seq[:4], "run":raw_animation_seq[4:] }
        self.offset=(64//2, 96//2)




        self.anim_tick=0
        self.anim_rate=0.1

        self.state="idle"
        self.facing=0




    def update(self, keys, dt):

        self.state="idle"
        if keys[pygame.K_s]:self.vel[1], self.state = min(self.vel[1]+self.accel*dt, self.speed), "run"
        if keys[pygame.K_w]:self.vel[1], self.state = max(self.vel[1]-self.accel*dt, -self.speed), "run"
        if keys[pygame.K_d]:self.vel[0], self.state, self.facing = min(self.vel[0]+self.accel*dt, self.speed), "run", 0
        if keys[pygame.K_a]:self.vel[0], self.state, self.facing = max(self.vel[0]-self.accel*dt, -self.speed), "run", 1



        self.vel[0]-=self.vel[0]*self.friction_force*dt
        self.vel[1]-=self.vel[1]*self.friction_force*dt

        self.pos[0]+=self.vel[0]*dt
        self.pos[1]+=self.vel[1]*dt


        self.rot+=dt

        if False:
            for i in range(15):
                angle=random.random()/2+self.rot
                self.particle_ref.append(particle(self.surface_ref, self.camera_ref, self.pos.copy(), [math.sin(angle)*random.randint(400,1500), math.cos(angle)*random.randint(400,1500)], COLOURS[random.randint(0,len(COLOURS)-1)], random.randint(2,5), 4  ))


        self.anim_tick+=dt


    def render(self):
        #self.surface_ref.blit(self.shadow, (self.pos[0]-self.camera_ref.render_pos[0]-self.shadow_offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.shadow_offset[1]))

        self.surface_ref.blit(self.animation_data[self.state][ int(self.anim_tick/self.anim_rate)%(len(self.animation_data[self.state])-1)  ][self.facing]  , (self.pos[0]-self.camera_ref.render_pos[0]-self.offset[0], self.pos[1]-self.camera_ref.render_pos[1]-self.offset[1]) )





class world:
    def __init__(self, surface_ref, map_size, density, tile_size):
        self.surface_ref=surface_ref
        self.map_data = [[ int((x%2)-(y%2)==0) for x in range(map_size[0])] for y in range(map_size[1]) ]
        self.map_size=map_size
        self.tile_size=tile_size

        self.map_rect=pygame.Rect(0,0,self.map_size[0]*self.tile_size, self.map_size[1]*self.tile_size)


        self.surface_size=surface_ref.get_size()

        self.particles=[]
        self.eggs=[]
        self.enemies=[]


        self.nest_pos=self.map_rect.center




        self.active_cam=camera( self.nest_pos, self.surface_size)

        self.active_player=player(surface_ref, self.active_cam, self.particles, self.nest_pos)

        self.active_cam.follow_mode(self.active_player.pos, 4)


        egg_images=load_tiles("assets/egg-Sheet.png", 4, (32,32), (40, 40))

        for i in range(4): self.eggs.append(egg(self.surface_ref, self.active_cam, self.active_player.pos,  egg_images[i],  (self.nest_pos[0]+random.randint(-40,40), self.nest_pos[1]+random.randint(-40,40))   ))

        for i in range(40): self.enemies.append(enemy(self.surface_ref, self.active_cam, self.particles, self.eggs, [random.randint(0,self.map_rect.width),  random.randint(0,self.map_rect.height)]    ))

    def update(self, keys, mouse_pos, mouse_state, dt):
        self.active_player.update(keys, dt)
        self.active_cam.update(keys, mouse_pos, mouse_state, dt)


        for e in self.enemies:
            e.update(dt)



        p=0
        while p <len(self.particles):
            if self.particles[p].update([0,0],dt): self.particles.pop(p)
            else:p+=1

        e=0
        while e <len(self.eggs):
            if self.eggs[e].update(dt): self.eggs.pop(e)
            else:e+=1



    def render(self):
        clip_start=[ clamp(int(   self.active_cam.render_pos[0]/self.tile_size)-1, 0, self.map_size[0] ) , clamp(int(self.active_cam.render_pos[1]//self.tile_size)-1, 0, self.map_size[1])]
        clip_end=[  clamp( int(  (self.active_cam.render_pos[0]+self.surface_size[0])//self.tile_size)+1, 0, self.map_size[0]), clamp(int(  (self.active_cam.render_pos[1]+self.surface_size[1])//self.tile_size )+1, 0, self.map_size[1]) ]

        for y in range(clip_start[1], clip_end[1]):
            for x in range(clip_start[0], clip_end[0]):
                pygame.draw.rect(self.surface_ref, CHECK_COLOURS[self.map_data[y][x]],
                                            pygame.Rect(x*self.tile_size-self.active_cam.render_pos[0], y*self.tile_size-self.active_cam.render_pos[1], self.tile_size, self.tile_size))


        self.active_player.render()

        for e in self.enemies:
            e.render()


        for e in self.eggs:
            e.render()


        for p in self.particles:
            p.render()



