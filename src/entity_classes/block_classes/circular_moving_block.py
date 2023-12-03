import pyglet
from src.helpers.utils import std_speed, block_width, gravity, make_sprite
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.sprite_collection import SpriteCollection
from src.entity_classes.block import Block
from src.helpers.globals import Direction
import time
import math


class MovingBlock(Block):
    def __init__(self, window, global_pos, radius, time, batch, start_right: bool = False, clockwise: bool = True):
        sprites = SpriteCollection(idle_right=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window),
                                                    visible=True,
                                                    batch=batch),
                                    idle_left=make_sprite(sprite_filename="assets/images/bbox.png",
                                                    width=block_width(window) * 2,
                                                    height=block_width(window),
                                                    visible=False,
                                                    batch=batch),)
        super().__init__(
            window=window,
            sprites=sprites,
            global_pos=global_pos,
            hitbox_width=block_width(window) * 2,
            hitbox_height=block_width(window),
            batch=batch,
        )

        self.speed = (block_width(window) * distance) / time  # we want to move one block per second
        self.starting_block_pos = self.block_pos
        self.time = time
        self.radius = radius
        self.start_right = start_right

        if start_right:
            self.global_pos.first += distance * block_width(window)
            self.direction = Direction.LEFT

    def copy(self):
        new_copy = MovingBlock(window=self.window,
                             global_pos=self.global_pos,
                             radius=self.radius,
                             time=self.time,
                             batch=self.batch,
                             start_right=self.start_right)
        
        return new_copy
    
    def pre_tick(self, dt: float):
        self.calculate_velocity()
        # if self.velocity.first > 0:
        #     self.direction = Direction.RIGHT
        # elif self.velocity.first < 0:
        #     self.direction = Direction.LEFT

    def tick(self, dt: float, camera_pos: Pair):
        super().tick(dt, camera_pos)

        if self.direction == Direction.RIGHT and self.block_pos.first - self.starting_block_pos.first >= self.distance:
            self.direction = Direction.LEFT
        elif self.direction == Direction.LEFT and self.block_pos.first - self.starting_block_pos.first <= 0:
            self.direction = Direction.RIGHT
    
    def calculate_velocity(self):
        self.velocity = Pair(0, self.velocity.second)
        speed = self.get_speed()
        # print(speed)
        self.velocity = Pair(self.velocity.first + speed, self.velocity.second)
    
    def get_speed(self):
        speed = self.speed
        if self.direction == Direction.LEFT:
            speed = -1 * speed
        
        return speed
    
    def get_location(self, angle):
        x = self.radius * math.cos(math.radians(angle))
        y = self.radius * math.sin(math.radians(angle))