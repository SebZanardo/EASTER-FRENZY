from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, game_manager) -> None:
        '''An abstract Scene'''
        self.game_manager = game_manager

    @abstractmethod
    def handle_event(self, event) -> None:
        '''Performs tasks for specified input'''
        pass

    @abstractmethod
    def update(self, dt) -> None:
        '''Update values and perform calculations'''
        pass

    @abstractmethod
    def render(self, surface) -> None:
        '''Render scene elements'''
        pass
