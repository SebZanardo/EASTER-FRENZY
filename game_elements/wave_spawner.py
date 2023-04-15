import math
import random

from game_elements.enemy import Enemy

class WaveSpawner:
    def __init__(self, x, y, radius, enemy_ref, particle_ref, camera_ref, eggs_ref, player_weapon, map_dim):
        self.x = x
        self.y = y
        self.radius = radius
        self.enemy_ref = enemy_ref
        self.particle_ref = particle_ref
        self.camera_ref = camera_ref
        self.eggs_ref = eggs_ref
        self.player_weapon = player_weapon
        self.map_dim = map_dim


        self.time_until_next_spawn = 7 # seconds (float)
        self.enemies_per_spawn = 3 # amount (int)

        self.timer = self.time_until_next_spawn # counts down to 0

    def update(self, dt):
        self.timer -= dt

        # SPAWN ENEMIES!
        if self.timer <= 0:
            for i in range(self.enemies_per_spawn):
                angle = random.random() * 2 * math.pi # random angle between 0 and 2PI
                pos = (math.sin(angle)*self.radius + self.x, math.cos(angle)*self.radius+ self.y)

                # instantiate enemy and add to array
                self.enemy_ref.append(Enemy(pos, self.camera_ref, self.particle_ref, self.eggs_ref, self.player_weapon, self.map_dim))

            self.timer = self.time_until_next_spawn

