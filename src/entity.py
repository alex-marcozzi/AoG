import pyglet
from src.utils import add_tuples

class Entity:
    def __init__(self, window, sprite_filename: str, global_pos: tuple, velocity: tuple, acceleration: tuple):
        self.window = window
        self.sprite = pyglet.resource.image(sprite_filename)
        self.global_pos = global_pos
        self.velocity = velocity
        self.acceleration = acceleration

    def tick(self):
        self.global_pos = add_tuples(self.global_pos, self.velocity)
        self.velocity = add_tuples(self.velocity, self.acceleration)

    def draw(self, camera_pos):
        print(self.global_pos[0] - camera_pos[0])
        #self.screen_mapping[self.current_screen].draw()
        self.sprite.blit(self.global_pos[0] - camera_pos[0], self.global_pos[1] - camera_pos[1])