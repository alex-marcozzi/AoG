import pyglet
from src.helpers.utils import block_width, std_speed, gravity

class Context:
    def __init__(self, window: pyglet.window.Window):
        self.window = window
        self.block_w = block_width(window)
        self.std_speed = std_speed(window)
        self.gravity = gravity(window)
        self.batch = None
        self.keys_down = {}
        self.keys_usable = {}