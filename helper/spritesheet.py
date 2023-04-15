import pygame


COLOUR_KEY = (255,0,255) # RGB value will not appear when drawing sprites

class SpriteSheet:
    def __init__(self, file_path: str, sprite_dim: tuple, upscale_dim=None, flip=False) -> None:
        '''Holds a spritesheet and associated sprite surfaces'''
        self.file_path = file_path
        self.sprite_dim=sprite_dim
        self.upscale_dim=upscale_dim
        self.flip=flip

        self.sprite_sheet = pygame.image.load(file_path).convert_alpha()

    def slice_sheet(self) -> dict[pygame.Surface]:
        '''Returns a dictionary of all sprites in the sprite sheet'''
        sprites = {}

        rows = int(self.sprite_sheet.get_height()/self.sprite_dim[0])
        columns = int(self.sprite_sheet.get_width()/self.sprite_dim[1])

        for y in range(rows):
            for x in range(columns):
                temp_sprite = self.get_sprite(x*self.sprite_dim[0], y*self.sprite_dim[1])
                sprites[int(y*columns+x)] = (temp_sprite, pygame.transform.flip(temp_sprite,1,0)) if self.flip else temp_sprite

        return sprites

    def get_sprite(self, x: int, y: int, ) -> pygame.Surface:
        '''Returns a pygame surface with sprite at location (x, y) drawn on it'''
        new_sprite = pygame.Surface((self.sprite_dim[0], self.sprite_dim[1]), pygame.SRCALPHA)
        
        new_sprite.blit(self.sprite_sheet, (0,0), (x, y, self.sprite_dim[0], self.sprite_dim[1]))
        new_sprite=new_sprite.convert_alpha()
        return new_sprite if not self.upscale_dim else pygame.transform.scale(new_sprite, self.upscale_dim)