import pyglet
from src.helpers.utils import std_speed
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.entity_classes.character import Character
from src.helpers.globals import Direction
import time

class Player(Character):
    def __init__(self, window, sprite_filename: str, global_pos: Pair, velocity: Pair, acceleration: Pair, width: float, height: float):
        super().__init__(window, sprite_filename, global_pos, velocity, acceleration, width, height, hp=3)

        # self.standard_speed = std_speed(window)
        self.keys_down = {}
        self.keys_usable = {}
        self.immunity_start = None
        self.immunity_duration_seconds = 1
    
    def pre_tick(self):
        super().pre_tick()
        self.check_keys()

    # def tick(self, camera_pos: Pair):
    #     super().tick(camera_pos)

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)
            if direction == Direction.DOWN:
                self.keys_usable[pyglet.window.key.SPACE] = True
        if "dangerous" in entity.modifiers:
            now = time.time()
            if not self.immunity_start or now - self.immunity_start > self.immunity_duration_seconds:
                self.interact_dangerous(entity, direction)
                self.immunity_start = time.time()  # epoch time
    
    def handle_key_press(self, symbol, modifiers):
        self.keys_down[symbol] = True

    def handle_key_release(self, symbol, modifiers):
        self.keys_down[symbol] = False
    
    def check_keys(self):
        if self.keys_down.get(pyglet.window.key.A, False):
            self.velocity = Pair(self.velocity.first - self.standard_speed, self.velocity.second)
        if self.keys_down.get(pyglet.window.key.D, False):
            self.velocity = Pair(self.velocity.first + self.standard_speed, self.velocity.second)
        if self.keys_down.get(pyglet.window.key.SPACE, False) and self.keys_usable.get(pyglet.window.key.SPACE, True):
            self.velocity = Pair(self.velocity.first, self.velocity.second + (self.block_w / 5))
            self.keys_usable[pyglet.window.key.SPACE] = False