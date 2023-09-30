import pyglet
from src.helpers.utils import std_speed
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.helpers.globals import Direction 

class Player(Entity):
    def __init__(self, window, sprite_filename: str, global_pos: Pair, velocity: Pair, acceleration: Pair, width: float, height: float):
        super().__init__(window, sprite_filename, global_pos, velocity, acceleration, width, height)

        self.standard_speed = std_speed(window)
        self.keys_down = {}
        self.keys_usable = {}
    
    def tick(self, camera_pos: Pair):
        super().tick(camera_pos)

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            if direction == Direction.DOWN:
                self.global_pos = Pair(self.global_pos.first, entity.global_pos.second + entity.sprite.height)
                self.velocity = Pair(self.velocity.first, 0)
                self.keys_usable[pyglet.window.key.SPACE] = True
            if direction == Direction.RIGHT:
                if self.block_pos.first + 1 == entity.block_pos.first and self.block_pos.second - 1 == entity.block_pos.second:
                    return
                print("! RIGHT COLLISION")
                self.global_pos = Pair(entity.global_pos.first - self.sprite.width, self.global_pos.second)
                self.velocity = Pair(0, self.velocity.second)
            if direction == Direction.LEFT:
                if self.block_pos.first - 1 == entity.block_pos.first and self.block_pos.second - 1 == entity.block_pos.second:
                    return
                print("! LEFT COLLISION")
                self.global_pos = Pair(entity.global_pos.first + entity.sprite.width, self.global_pos.second)
                self.velocity = Pair(0, self.velocity.second)
            if direction == Direction.UP:
                print("! UP COLLISION")
                self.global_pos = Pair(self.global_pos.first, entity.global_pos.second - self.sprite.height)
                self.velocity = Pair(self.velocity.first, 0)

        pass
    
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