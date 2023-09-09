import pyglet
from src.helpers.utils import add_tuples

loaded_images = {}  # key: filename, value: image

class Entity:
    def __init__(self, window, sprite_filename: str, global_pos: tuple, velocity: tuple, acceleration: tuple, width: float, height: float):
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

    def tick(self, camera_pos):
        self.global_pos = add_tuples(self.global_pos, self.velocity)
        self.velocity = add_tuples(self.velocity, self.acceleration)

        self.sprite.x = self.global_pos[0] - (camera_pos[0] - (self.window.width / 2))
        self.sprite.y = self.global_pos[1] - (camera_pos[1] - (self.window.height / 2))

    def draw(self):
        self.sprite.draw()