import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.projectile import Projectile
from src.helpers.globals import Direction
import time


class Lightning(Projectile):
    def __init__(self, window, global_pos, batch):
        self.speed = std_speed(window) * 2

        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=block_width(window) / 2,
                                                    height=block_width(window) / 2,
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=block_width(window) / 2,
                                                    height=block_width(window) / 2,
                                                    visible=False,
                                                    batch=batch),)
        super().__init__(
            window=window,
            sprites=sprites,
            global_pos=global_pos,
            velocity=Pair(self.speed, 0),
            acceleration=Pair(0, 0),
            range=block_width(window) * 5,
            hitbox_width=block_width(window) / 2,
            hitbox_height=block_width(window) / 2,
            batch=batch,
        )

        self.modifiers = ["dangerous"]

    def copy(self):
        new_copy = Lightning(window=self.window,
                             global_pos=self.global_pos,
                             batch=self.batch,)
        
        return new_copy

    # def pre_tick(self, dt: float):
    #     super().pre_tick(dt)
    #     speed = self.speed * self.get_speed()
    #     # print(speed)
    #     self.velocity = Pair(self.velocity.first + speed, self.velocity.second)
