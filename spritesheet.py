import pygame


COLOUR_KEY = (255,0,255) # RGB value will not appear when drawing sprites

class SpriteSheet:
    def __init__(self, file_path: str, sprite_width: int, sprite_height: int) -> None:
        '''Holds a spritesheet and associated sprite surfaces'''
        self.file_path = file_path
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height

        self.sprite_sheet = pygame.image.load(file_path).convert_alpha()

    def slice_sheet(self) -> dict[pygame.Surface]:
        '''Returns a dictionary of all sprites in the sprite sheet'''
        sprites = {}

        rows = int(self.sprite_sheet.get_height()/self.sprite_height)
        columns = int(self.sprite_sheet.get_width()/self.sprite_width)

        for y in range(rows):
            for x in range(columns):
                sprites[int(y*columns+x)] = self.get_sprite(x*self.sprite_width, y*self.sprite_height)

        return sprites

    def get_sprite(self, x: int, y: int) -> pygame.Surface:
        '''Returns a pygame surface with sprite at location (x, y) drawn on it'''
        new_sprite = pygame.Surface((self.sprite_width, self.sprite_height))
        new_sprite.fill(COLOUR_KEY)
        new_sprite.set_colorkey(COLOUR_KEY)
        new_sprite.blit(self.sprite_sheet, (0,0), (x, y, self.sprite_width, self.sprite_height))
        return new_sprite
