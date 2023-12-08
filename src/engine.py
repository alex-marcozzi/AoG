import pyglet
from src.gameplay_sreen import GameplayScreen
from src.helpers.context import Context


class Engine:
    def __init__(self, context: Context):
        self.screen_mapping = {
            "STARTUP": "startup_screen_class_goes_here",
            "TITLE": "title_screen_class_goes_here",
            "PAUSE": "pause_screen_class_goes_here",
            "GAME": GameplayScreen(context),
        }

        self.current_screen = "GAME"
        self.context = context

    def tick(self, dt: float):
        self.screen_mapping[self.current_screen].tick(dt)

    def draw(self):
        self.screen_mapping[self.current_screen].draw()

    def handle_key_press(self, symbol, modifiers):
        print(f"* pressing key {symbol}")
        self.context.keys_down[symbol] = True
        # self.screen_mapping[self.current_screen].handle_key_press(symbol, modifiers)

    def handle_key_release(self, symbol, modifiers):
        print(f"^ releasing key {symbol}")
        self.context.keys_down[symbol] = False
        # self.screen_mapping[self.current_screen].handle_key_release(symbol, modifiers)
