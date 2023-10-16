import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.character import Character
from src.helpers.globals import Direction
import time


class Bear(Character):
    def __init__(self, window, global_pos, batch):
        self.speed = std_speed(window) / 2.0

        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window) * 2,
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/bear.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window) * 2,
                                                    visible=False,
                                                    batch=batch),)
        super().__init__(
            window=window,
            sprites=sprites,
            global_pos=global_pos,
            velocity=Pair(-1 * self.speed, 0),
            acceleration=Pair(0, gravity(window)),
            # sprite_width=block_width(window) * 2,
            # sprite_height=block_width(window) * 2,
            hitbox_width=block_width(window) * 2,
            hitbox_height=block_width(window) * 2,
            batch=batch,
            hp=1,
        )

        self.modifiers = ["dangerous"]
        self.move_loop_start = time.time()
        self.left = True

    def pre_tick(self, dt: float):
        super().pre_tick(dt)
        speed = self.speed * self.get_speed()
        # print(speed)
        self.velocity = Pair(self.velocity.first + speed, self.velocity.second)

    # def tick(self, camera_pos: Pair):
    #     super().tick(camera_pos)
    #     self.velocity = Pair(self.velocity.first - self.speed, self.velocity.second)

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)
        if "dangerous" in entity.modifiers:
            self.interact_dangerous(entity, direction)

    # function: y = 1 - (2x - 1)^2
    # x: time
    # y: speed
    def get_speed(self):
        now = time.time()
        x = (now - self.move_loop_start) / 3.0
        y = 1 - (((2 * x) - 1) ** 2)
        y *= -1 if self.left else 1

        if x >= 1:
            self.move_loop_start = now
            self.left = not self.left

        return y
