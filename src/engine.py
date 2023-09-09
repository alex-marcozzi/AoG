import pyglet
from src.gameplay_sreen import GameplayScreen

class Engine:
    def __init__(self, window):
        self.screen_mapping = {
            "STARTUP": "startup_screen_class_goes_here",
            "TITLE": "title_screen_class_goes_here",
            "PAUSE": "pause_screen_class_goes_here",
            "GAME": GameplayScreen(window),
        }

        self.current_screen = "GAME"
        self.window = window
    
    def tick(self):
        self.screen_mapping[self.current_screen].tick()

    def draw(self):
        self.screen_mapping[self.current_screen].draw()

    def handle_key_press(self, symbol, modifiers):
        self.screen_mapping[self.current_screen].handle_key_press(symbol, modifiers)

    def handle_key_release(self, symbol, modifiers):
        self.screen_mapping[self.current_screen].handle_key_release(symbol, modifiers)
