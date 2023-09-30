import pyglet
from src.helpers.utils import std_speed, gravity, block_width
from src.helpers.physics import is_down_collision, is_right_collision, is_left_collision, is_up_collision
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.helpers.globals import Direction

# this is basically all of the level information, like a context
class World:
    def __init__(self, window: pyglet.window.Window, level: list, player: Entity) -> None:
        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        self.level = level
        # self.player = Entity(window,
        #                      "assets/images/goose.png",
        #                      global_pos=Pair(0, 200),
        #                      velocity=Pair(0, 0),
        #                      acceleration=Pair(0, gravity(window)),
        #                      width=self.block_w,
        #                      height=self.block_w * 2)
        self.characters = [player]
        self.player = player

    # def tick(self):
    #     self.do_physics
    
    def do_physics(self, from_loc: int, to_loc: int):
        for y in range(0, len(self.level[0])):
            for x in range(from_loc, to_loc):
                block = self.level[x][y]
                if issubclass(type(block), Entity):
                    # collisions = self.check_collisions(block)

                    # for collision in collisions:
                    #     # self.handle_collision(block, collision.first, collision.second)
                    #     block.interact(collision.first, collision.second)

                    block.tick(self.player.global_pos)
                    
        
        for character in self.characters:
            if issubclass(type(character), Entity):
                collisions = self.check_collisions(character)

                for collision in collisions:
                    # self.handle_collision(character, collision.first, collision.second)
                    character.interact(collision.first, collision.second)

                character.tick(self.player.global_pos)
                


    # def handle_collision(self, entity1: Entity, entity2: Entity, direction):
    #     if direction == Direction.DOWN:
    #         entity1.interact(entity2, direction)



    def check_collisions(self, entity: Entity):
        # player_block_pos = Pair(self.player.global_pos.first // self.block_w, self.player.global_pos.second // block_h)

        # the three squares below the entity
        # to_check = [Pair(entity.block_pos.first - 1, entity.block_pos.second - 1),  # behind and below
        #             Pair(entity.block_pos.first, entity.block_pos.second - 1),  # straight below
        #             Pair(entity.block_pos.first + 1, entity.block_pos.second - 1)]  # infront and below

        to_check = []

        # check square around the entity
        for y in range(-1, 3, 1):
            for x in range(-1, 3, 1):
                to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second + y))
        
        collisions = []
        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if type(block) is Entity:
                if is_down_collision(entity, block):
                    collisions.append(Pair(block, Direction.DOWN))
                if is_right_collision(entity, block):
                    collisions.append(Pair(block, Direction.RIGHT))
                if is_left_collision(entity, block):
                    collisions.append(Pair(block, Direction.LEFT))
                if is_up_collision(entity, block):
                    collisions.append(Pair(block, Direction.UP))
        
        return collisions