class Camera:
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


    def update(self, mouse_pos, dt):
        if self.mode:
            if self.mode=="follow":
                self.pos_raw=( self.pos_raw[0]-(self.pos_raw[0]-self.follow_target[0])*dt*self.speed, self.pos_raw[1]-(self.pos_raw[1]-self.follow_target[1])*dt*self.speed  )
                self.pos=(self.pos_raw[0]+(mouse_pos[0]-self.render_offset[0])/6, 
                            self.pos_raw[1]+(mouse_pos[1]-self.render_offset[1])/6)

        self.render_pos=(self.pos[0]-self.render_offset[0], self.pos[1]-self.render_offset[1])


