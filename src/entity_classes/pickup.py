import pyglet
from src.helpers.utils import std_speed, block_width, make_sprite
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.attack import Attack
from src.sprite_collection import SpriteCollection
from src.helpers.globals import Direction
import time

class Pickup(Entity):
    def __init__(
        self,
        window,
        sprites: SpriteCollection,
        global_pos: Pair,
        hitbox_width: float,
        hitbox_height: float,
        batch,
    ):
        self.sprites = sprites
        self.sprites.SetVisible(self.sprites.idle_right)
        
        super().__init__(
            window,
            sprites,
            global_pos,
            hitbox_width,
            hitbox_height,
            batch,
        )
        self.direction = Direction.RIGHT
        self.modifiers = []

    def copy(self):
        new_copy = Pickup(window=self.window,
                             sprites=self.sprites.copy(),
                             global_pos=self.global_pos,
                             hitbox_width=self.hitbox.width,
                             hitbox_height=self.hitbox.height,
                             batch=self.batch)
        
        return new_copy

    def pre_tick(self, dt: float):
        self.velocity = Pair(0, self.velocity.second)

    def tick(self, dt: float, camera_pos: Pair):
        super().tick(dt, camera_pos)