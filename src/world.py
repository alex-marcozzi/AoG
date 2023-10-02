import pyglet
from src.helpers.utils import std_speed, gravity, block_width
from src.helpers.physics import is_down_collision, is_right_collision, is_left_collision, is_up_collision
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.entity_classes.character import Character
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
        self.extract_characters(self.level)
        print(len(self.characters))

    # def tick(self):
    #     self.do_physics

    def extract_characters(self, level: list):
        for x in range(len(level)):
            for y in range(len(level[x])):
                if issubclass(type(level[x][y]), Entity):
                    print(f"{x}, {y}: {type(level[x][y])}")
                    if issubclass(type(level[x][y]), Character):
                        print("HERE")
                        self.characters.append(level[x][y])
                        level[x][y] = None
    
    def do_physics(self, from_loc: int, to_loc: int):
        index = 0
        for character in self.characters:
            if issubclass(type(character), Entity):
                collisions = self.check_collisions(character)

                for collision in collisions:
                    # self.handle_collision(character, collision.first, collision.second)
                    character.interact(collision.first, collision.second)

                if not character.tick(self.player.global_pos):
                    self.characters.pop(index)
            index += 1

        for y in range(0, len(self.level[0])):
            for x in range(from_loc, to_loc):
                block = self.level[x][y]
                if issubclass(type(block), Entity):
                    # collisions = self.check_collisions(block)

                    # for collision in collisions:
                    #     # self.handle_collision(block, collision.first, collision.second)
                    #     block.interact(collision.first, collision.second)

                    block.tick(self.player.global_pos)
                    

                


    # def handle_collision(self, entity1: Entity, entity2: Entity, direction):
    #     if direction == Direction.DOWN:
    #         entity1.interact(entity2, direction)



    def check_collisions(self, entity: Entity):
        collisions = []
        
        for character in self.characters:
            if character == entity:
                continue
            # print(f"Entity: {entity.global_pos.first}, {entity.global_pos.second}")
            # print(f"Charac: {character.global_pos.first}, {character.global_pos.second}")
            if is_down_collision(entity, character):
                print("CHARACTER DOWN COLLISION")
                collisions.append(Pair(character, Direction.DOWN))
            if is_right_collision(entity, character):
                print("CHARACTER RIGHT COLLISION")
                collisions.append(Pair(character, Direction.RIGHT))
            if is_left_collision(entity, character):
                print("CHARACTER LEFT COLLISION")
                collisions.append(Pair(character, Direction.LEFT))
            if is_up_collision(entity, character):
                print("CHARACTER UP COLLISION")
                collisions.append(Pair(character, Direction.UP))

        to_check = []

        # check square around the entity
        for y in range(-1, 3, 1):
            for x in range(-1, 3, 1):
                to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second + y))
        
        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_down_collision(entity, block):
                    collisions.append(Pair(block, Direction.DOWN))
                if is_right_collision(entity, block):
                    collisions.append(Pair(block, Direction.RIGHT))
                if is_left_collision(entity, block):
                    collisions.append(Pair(block, Direction.LEFT))
                if is_up_collision(entity, block):
                    collisions.append(Pair(block, Direction.UP))
        
        return collisions