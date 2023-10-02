import pyglet
from src.helpers.utils import std_speed
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.helpers.globals import Direction 

class Character(Entity):
    def __init__(self, window, sprite_filename: str, global_pos: Pair, velocity: Pair, acceleration: Pair, width: float, height: float, hp: int):
        super().__init__(window, sprite_filename, global_pos, velocity, acceleration, width, height)

        self.hp = hp
        # self.standard_speed = std_speed(window)
    
    def tick(self, camera_pos: Pair):
        super().tick(camera_pos)

        if self.hp <= 0:
            return False
        
        return True

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)
    
    def interact_collidable(self, entity: Entity, direction):
        if direction == Direction.DOWN:
            self.global_pos = Pair(self.global_pos.first, entity.global_pos.second + entity.sprite.height)
            self.velocity = Pair(self.velocity.first, 0)
        if direction == Direction.RIGHT:
            if not issubclass(type(entity), Character) and self.block_pos.first + 1 == entity.block_pos.first and self.block_pos.second - 1 == entity.block_pos.second:
                return
            print("! RIGHT COLLISION")
            self.global_pos = Pair(entity.global_pos.first - self.sprite.width, self.global_pos.second)
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.LEFT:
            if not issubclass(type(entity), Character) and self.block_pos.first - 1 == entity.block_pos.first and self.block_pos.second - 1 == entity.block_pos.second:
                return
            print("! LEFT COLLISION")
            self.global_pos = Pair(entity.global_pos.first + entity.sprite.width, self.global_pos.second)
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.UP:
            print("! UP COLLISION")
            self.global_pos = Pair(self.global_pos.first, entity.global_pos.second - self.sprite.height)
            self.velocity = Pair(self.velocity.first, 0)
