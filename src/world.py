import pyglet
from src.helpers.utils import std_speed, gravity, block_width
from src.helpers.physics import (
    is_down_collision,
    is_right_collision,
    is_left_collision,
    is_up_collision,
    is_overlap,
)
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.hitbox import Hitbox
from src.entity_classes.character import Character
from src.entity_classes.player import Player
from src.helpers.globals import Direction

# this is basically all of the level information, like a context
class World:
    def __init__(self, window: pyglet.window.Window, level: list, batch) -> None:
        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        self.level = level
        self.player = Player(
            window,
            "assets/images/goose.png",
            global_pos=Pair(0, 500),
            velocity=Pair(0, 0),
            acceleration=Pair(0, gravity(window)),
            sprite_width=self.block_w,
            sprite_height=self.block_w * 1,
            hitbox_width=self.block_w,
            hitbox_height=self.block_w,
            batch=batch,
        )
        self.characters = [self.player]
        self.extract_characters(self.level)

    # def tick(self):
    #     self.do_physics

    def extract_characters(self, level: list):
        for x in range(len(level)):
            for y in range(len(level[x])):
                if issubclass(type(level[x][y]), Entity):
                    level[x][y].tick(
                        self.player.global_pos
                    )  # first tick is necessary to set the entities' positions
                    if issubclass(type(level[x][y]), Character):
                        # print("HERE")
                        self.characters.append(level[x][y])
                        level[x][y] = None

    def do_physics(self, from_loc: int, to_loc: int):
        index = 0
        for character in self.characters:
            # if abs(character.block_pos.first - self.player.block_pos.first) >= 12:
            #     continue
            if issubclass(type(character), Character):
                character.pre_tick()
                collisions = self.check_collisions(character)

                character.on_ground = False
                for collision in collisions:
                    if collision.second == Direction.DOWN:
                        character.on_ground = True

                    character.interact(collision.first, collision.second)
                
                # some characters don't have an attack
                if character.attack:
                    self.check_attacks(character)

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
            if is_overlap(entity, character):
                if entity == self.player:
                    print("CHARACTER OVERLAP")
                collisions.append(Pair(character, Direction.OVERLAP))

        to_check = []

        # check square around the entity
        for y in range(-1, 3, 1):
            for x in range(-1, 3, 1):
                to_check.append(
                    Pair(entity.block_pos.first + x, entity.block_pos.second + y)
                )

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

    def check_attacks(self, character: Character):
        if not character.attack.inProgress():
            return []
        
        # check the attack hitbox against all other characters
        for other_character in self.characters:
            if other_character == character:
                continue

            for attack_hitbox in character.attack.hitboxes:
                pos = Pair(character.global_pos.first + attack_hitbox.pos.first,
                                         character.global_pos.second + attack_hitbox.pos.second)
                true_hitbox = Hitbox(pos=pos, width=attack_hitbox.width, height=attack_hitbox.width)
                if is_overlap(true_hitbox, other_character.hitbox):
                    # character.attack.Hit(other_character)
                    other_character.takeHit(character.attack)
