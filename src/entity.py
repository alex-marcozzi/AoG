import pyglet
from src.helpers.interfaces import Pair
from src.helpers.utils import block_width, std_speed
from src.helpers.globals import Direction

loaded_images = {}  # key: filename, value: image

class Entity:
    def __init__(self, window, sprite_filename: str, global_pos: Pair, velocity: Pair, acceleration: Pair, width: float, height: float):
        self.window = window
        self.standard_speed = std_speed(window)
        self.block_w = block_width(window)
        if not sprite_filename in loaded_images.keys():
            loaded_images[sprite_filename] = pyglet.resource.image(sprite_filename)
        self.sprite = pyglet.sprite.Sprite(img=loaded_images[sprite_filename])
        self.sprite_filename = sprite_filename
        self.sprite.width = width
        self.sprite.height = height
        self.global_pos = global_pos.copy()
        self.block_pos = Pair(self.global_pos.first // self.block_w, self.global_pos.second // self.block_w)
        self.velocity = velocity.copy()
        self.acceleration = acceleration.copy()
        self.modifiers = ["collidable"]

    def copy(self):
        new_copy = Entity(window=self.window,
                          sprite_filename=self.sprite_filename,
                          global_pos=self.global_pos,
                          velocity=self.velocity,
                          acceleration=self.acceleration,
                          width=self.sprite.width,
                          height=self.sprite.height)
        return new_copy

    def tick_pos_only(self):
        self.global_pos.add(self.velocity)
        # self.velocity.add(self.acceleration)

    def tick(self, camera_pos: Pair):
        self.global_pos.add(self.velocity)
        self.velocity.add(self.acceleration)

        # camera_pos == player.global_pos (middle of screen)
        self.sprite.x = self.global_pos.first - (camera_pos.first - (self.window.width / 2))
        self.sprite.y = self.global_pos.second - (camera_pos.second - (self.window.height / 2))
        self.block_pos = Pair(self.global_pos.first // self.block_w, (self.global_pos.second + 10) // self.block_w)

    def draw(self):
        self.sprite.draw()

    def interact(self, entity: "Entity", direction):
        if "collidable" in entity.modifiers:
            if direction == Direction.DOWN:
                self.global_pos = Pair(self.global_pos.first, entity.global_pos.second + entity.sprite.height)
                self.velocity = Pair(self.velocity.first, 0)

        pass

    def nextPos(self):
        return Pair(self.global_pos.first + self.velocity.first, self.global_pos.second + self.velocity.second)
    
    def bottomLeft(self):
        return self.global_pos
    
    def bottomRight(self):
        return Pair(self.global_pos.first + self.sprite.width, self.global_pos.second)
    
    def topLeft(self):
        return Pair(self.global_pos.first, self.global_pos.second + self.sprite.height)
    
    def topRight(self):
        return Pair(self.global_pos.first + self.sprite.width, self.global_pos.second + self.sprite.height)