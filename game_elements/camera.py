import math

class Camera:
    def __init__(self, pos, camera_size):
        self.pos=pos
        self.camera_size=camera_size
        self.render_offset=[camera_size[0]//2, camera_size[1]//2]
        
        self.mode=None
        self.speed=None
        self.bounds=None

        self.shake_amount=0
        self.shake_fade=8

        self.shake_tick=0

    def follow_mode(self, target, speed=1):
        self.mode="follow"
        self.follow_target=target
        self.speed=speed
        self.pos_raw=self.pos

    def set_bounds(self, bounds_start, bounds_end):
        self.bounds=((bounds_start[0], bounds_end[0]), (bounds_start[1], bounds_end[1])   )


    def update(self, mouse_pos, dt):
        if self.mode:
            if self.mode=="follow":
                self.pos_raw=( self.pos_raw[0]-(self.pos_raw[0]-self.follow_target[0])*dt*self.speed, self.pos_raw[1]-(self.pos_raw[1]-self.follow_target[1])*dt*self.speed  )
                
                if self.bounds: self.pos_raw=(max(min(self.pos_raw[0], self.bounds[0][1]), self.bounds[0][0])  , max(min(self.pos_raw[1], self.bounds[1][1]), self.bounds[1][0]))

                self.pos=(self.pos_raw[0]+(mouse_pos[0]-self.render_offset[0])/6   +  math.sin(self.shake_tick*129.8+0.765)*self.shake_amount, 
                            self.pos_raw[1]+(mouse_pos[1]-self.render_offset[1])/6   +  math.sin(self.shake_tick*100)*self.shake_amount )

        self.render_pos=(round(self.pos[0]-self.render_offset[0]), round(self.pos[1]-self.render_offset[1]))


        self.shake_tick+=dt

        self.shake_amount=max(self.shake_amount-dt*self.shake_fade,   0)


