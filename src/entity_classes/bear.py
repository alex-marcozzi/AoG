import pyglet
from src.helpers.utils import std_speed, block_width, gravity
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.entity_classes.character import Character
from src.helpers.globals import Direction 

class Bear(Character):
    def __init__(self, window):
        super().__init__(window, "assets/images/bear.png", Pair(0, 0), Pair(0, 0), Pair(0, gravity(window)), block_width(window) * 2, block_width(window) * 2, hp=1)

        self.modifiers = ["collidable", "dangerous"]
    
    # def tick(self, camera_pos: Pair):
    #     super().tick(camera_pos)

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)