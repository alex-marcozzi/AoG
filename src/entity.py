import pyglet
from src.helpers.interfaces import Pair

loaded_images = {}  # key: filename, value: image

class Entity:
    def __init__(self, window, sprite_filename: str, global_pos: Pair, velocity: Pair, acceleration: Pair, width: float, height: float):
        self.window = window
        if not sprite_filename in loaded_images.keys():
            loaded_images[sprite_filename] = pyglet.resource.image(sprite_filename)
        self.sprite = pyglet.sprite.Sprite(img=loaded_images[sprite_filename])
        self.sprite_filename = sprite_filename
        self.sprite.width = width
        self.sprite.height = height
        self.global_pos = global_pos
        self.velocity = velocity
        self.acceleration = acceleration
        self.modifiers = ["collidable"]

    def copy(self):
        new_copy = Entity(self.window, self.sprite_filename, self.global_pos, self.velocity, self.acceleration, self.sprite.width, self.sprite.height)
        return new_copy

    def tick(self, camera_pos: Pair):
        self.global_pos.add(self.velocity)
        self.velocity.add(self.acceleration)

        # camera_pos == player.global_pos (middle of screen)
        self.sprite.x = self.global_pos.first - (camera_pos.first - (self.window.width / 2))
        self.sprite.y = self.global_pos.second - (camera_pos.second - (self.window.height / 2))

    def draw(self):
        self.sprite.draw()