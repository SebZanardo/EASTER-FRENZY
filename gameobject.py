from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, x, y, sprite, camera_ref) -> None:
        '''An abstract GameObject'''
        self.x = x
        self.y = y
        self.sprite = sprite
        self.camera_ref = camera_ref # remove?

    @abstractmethod
    def update(self, dt) -> None:
        '''Updates object values and perform calculations'''
        pass

    @abstractmethod
    def render(self, surface) -> None:
        '''Renders sprite to surface'''
        pass
