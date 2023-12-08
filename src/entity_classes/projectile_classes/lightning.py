import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.projectile import Projectile
from src.helpers.globals import Direction
import time


class Lightning(Projectile):
    def __init__(self, context: Context, global_pos, angle: float):
        self.speed = context.std_speed * 2
        self.angle = angle

        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=context.block_w / 2,
                                                    height=context.block_w / 2,
                                                    visible=True,
                                                    batch=context.batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/orange.png",
                                                    width=context.block_w / 2,
                                                    height=context.block_w / 2,
                                                    visible=False,
                                                    batch=context.batch),)
        super().__init__(
            context=context,
            sprites=sprites,
            global_pos=global_pos,
            speed=self.speed,
            angle=angle,
            # velocity=Pair(self.speed, 0),
            # acceleration=Pair(0, 0),
            range=context.block_w * 10,
            hitbox_width=context.block_w / 2,
            hitbox_height=context.block_w / 2,
            piercing=False
        )

        self.modifiers = ["dangerous"]

    def copy(self):
        new_copy = Lightning(context=self.context,
                             global_pos=self.global_pos,
                             angle=self.angle,)
        
        return new_copy

    # def pre_tick(self, dt: float):
    #     super().pre_tick(dt)
    #     speed = self.speed * self.get_speed()
    #     # print(speed)
    #     self.velocity = Pair(self.velocity.first + speed, self.velocity.second)
