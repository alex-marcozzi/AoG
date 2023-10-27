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
from src.entity_classes.projectile import Projectile

# this is basically all of the level information, like a context
class World:
    def __init__(self, window: pyglet.window.Window, level: list, batch) -> None:
        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        self.level = level
        self.player = Player(
            window,
            global_pos=Pair(0, 500),
            batch=batch,
        )
        self.characters = [self.player]
        self.projectiles: list[Projectile] = []
        self.extract_characters(self.level)

    # def tick(self):
    #     self.do_physics

    def extract_characters(self, level: list):
        for x in range(len(level)):
            for y in range(len(level[x])):
                if issubclass(type(level[x][y]), Entity):
                    level[x][y].tick(0, self.player.global_pos)  # first tick is necessary to set the entities' positions
                    if issubclass(type(level[x][y]), Character):
                        # print("HERE")
                        self.characters.append(level[x][y])
                        level[x][y] = None

    def do_physics(self, dt: float, from_loc: int, to_loc: int):
        # index = 0
        for character in self.characters:
            if abs(character.block_pos.first - self.player.block_pos.first) >= 12:
                continue
            if issubclass(type(character), Character):
                character.pre_tick(dt)  # set the character's velocity based on its movement pattern
                collisions = self.get_collisions(dt, character)

                self.process_collisions(character, collisions)
                
                # some characters don't have an attack
                if character.attack:
                    self.check_attacks(dt, character)

                if not character.tick(dt, self.player.global_pos):
                    character.sprites.SetAllInvisible()
                    self.characters.remove(character)
            # index += 1

        for projectile in self.projectiles:
            if not projectile.piercing and projectile.collided:
                self.projectiles.remove(projectile)
                continue

            projectile.tick(dt, self.player.global_pos)
            if projectile.isExpired():
                self.projectiles.remove(projectile)
            else:
                if not projectile.piercing:
                    collisions = self.get_collisions(dt, projectile)

                    for collision in collisions:
                        if not issubclass(type(collision.first), Projectile) and collision.second == Direction.OVERLAP and collision.first.id != projectile.owner_id:
                            # self.projectiles.remove(projectile)
                            projectile.collided = True
                            break
                    # if len(collisions) > 0:
                    #     self.projectiles.remove(projectile)

        for y in range(0, len(self.level[0])):
            for x in range(from_loc, to_loc):
                block = self.level[x][y]
                if issubclass(type(block), Entity):
                    # collisions = self.check_collisions(block)

                    # for collision in collisions:
                    #     # self.handle_collision(block, collision.first, collision.second)
                    #     block.interact(collision.first, collision.second)

                    block.tick(dt, self.player.global_pos)

    def get_collisions(self, dt: float, entity: Entity):
        collisions = []

        for character in self.characters:
            # if they are on the same team, they shouldn't be able to collide
            if character == entity:
                continue
            # if abs(character.block_pos.first - entity.block_pos.first) >= entity.block_pos.first + int(entity.hitbox.width / self.block_w) + 2:
            #     continue
            # print(f"Entity: {entity.global_pos.first}, {entity.global_pos.second}")
            # print(f"Charac: {character.global_pos.first}, {character.global_pos.second}")
            if is_down_collision(dt, entity, character):
                print("CHARACTER DOWN COLLISION")
                collisions.append(Pair(character, Direction.DOWN))
            if is_right_collision(dt, entity, character):
                print("CHARACTER RIGHT COLLISION")
                collisions.append(Pair(character, Direction.RIGHT))
            if is_left_collision(dt, entity, character):
                print("CHARACTER LEFT COLLISION")
                collisions.append(Pair(character, Direction.LEFT))
            if is_up_collision(dt, entity, character):
                print("CHARACTER UP COLLISION")
                collisions.append(Pair(character, Direction.UP))
            if is_overlap(dt, entity, character):
                if entity == self.player:
                    print("CHARACTER OVERLAP")
                collisions.append(Pair(character, Direction.OVERLAP))

        for projectile in self.projectiles:
            if projectile == entity or (issubclass(type(entity), Projectile) and projectile.owner_id == entity.owner_id) or entity.id == projectile.owner_id:
                continue
            if is_overlap(dt, entity, projectile):
                if entity == self.player:
                    print("PROJECTILE OVERLAP")
                collisions.append(Pair(projectile, Direction.OVERLAP))

        # check below for collisions
        to_check = []
        for x in range(0, int(entity.hitbox.width / self.block_w) + 1):
            to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second - 1))

        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_down_collision(dt, entity, block):
                    collisions.append(Pair(block, Direction.DOWN))

        # check right for collisions
        to_check = []
        for x in range(0, 2):
            for y in range(0, int(entity.hitbox.height / self.block_w) + 1):
                to_check.append(Pair(entity.block_pos.first + int(entity.hitbox.width / self.block_w) + x, entity.block_pos.second + y))

        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_right_collision(dt, entity, block):
                    collisions.append(Pair(block, Direction.RIGHT))

        # check left for collisions
        to_check = []
        # for x in range(-1, 1, 1):
        for y in range(0, int(entity.hitbox.height / self.block_w) + 1):
            to_check.append(Pair(entity.block_pos.first - 1, entity.block_pos.second + y))

        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_left_collision(dt, entity, block):
                    collisions.append(Pair(block, Direction.LEFT))

        # check up for collisions
        to_check = []
        for y in range(int(entity.hitbox.height / self.block_w), int(entity.hitbox.height / self.block_w) + 1):
            for x in range(0, int(entity.hitbox.width / self.block_w) + 1):
                to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second + y))

        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_up_collision(dt, entity, block):
                    collisions.append(Pair(block, Direction.UP))

        # check up for collisions
        to_check = [Pair(entity.block_pos.first, entity.block_pos.second)]
        # for y in range(int(entity.hitbox.height / self.block_w), int(entity.hitbox.height / self.block_w) + 3):
        #     for x in range(0, int(entity.hitbox.width / self.block_w) + 3):
        #         to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second + y))

        for loc in to_check:
            block = self.level[int(loc.first)][int(loc.second)]
            if issubclass(type(block), Entity):
                if is_overlap(dt, entity, block):
                    collisions.append(Pair(block, Direction.OVERLAP))

        return collisions
    
    def process_collisions(self, character: Character, collisions: list[Pair]):
        character.on_ground = False
        for collision in collisions:
            if collision.second == Direction.DOWN:
                character.on_ground = True

            if collision.second == Direction.UP and collision.first.id == self.player.id:
                if "bouncy" in character.modifiers:
                    self.player.jump()
                if "vulnerable_top" in character.modifiers:
                    character.interact_dangerous(collision.first, collision.second)
                else:
                    character.interact(collision.first, collision.second)
            else:
                character.interact(collision.first, collision.second)

    def check_attacks(self, dt: float, character: Character):
        if not character.attack.inProgress():
            return []
        
        # check the attack hitbox against all other characters
        for other_character in self.characters:
            if other_character == character:
                continue

            attack_hitbox = Hitbox(pos=character.bottomRight(), width=character.attack.range, height=character.hitbox.height)
            if character.direction == Direction.LEFT:
                attack_hitbox.pos.first = character.global_pos.first - character.attack.range

            if is_overlap(dt, attack_hitbox, other_character.hitbox):
                # character.attack.Hit(other_character)
                other_character.takeHit(character.attack)
        
        if character.attack.projectiles and not character.attack.has_fired_projectiles:
            for projectile in character.attack.projectiles:
                self.spawn_projectile(projectile, character)

            character.attack.has_fired_projectiles = True

    def spawn_projectile(self, projectile: Projectile, owner: Character):
        new_projectile = projectile.copy()
        spawn_pos = owner.global_pos.copy()
        spawn_pos.second += (owner.hitbox.height / 2) - (projectile.hitbox.height / 2)

        if owner.direction == Direction.RIGHT:
            spawn_pos.first += owner.hitbox.width + (self.block_w / 4)
        else:
            spawn_pos.first -= projectile.hitbox.width + (self.block_w / 4)
        
        new_projectile.spawn(spawn_pos, direction=owner.direction, owner_id=owner.id)
        # new_projectile.velocity.add(owner.velocity)
        self.projectiles.append(new_projectile)
