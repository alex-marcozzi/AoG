import pyglet
import sys
from src.helpers.utils import std_speed, gravity, block_width, make_sprite, hb_distance
from src.helpers.physics import (
    is_down_collision,
    is_right_collision,
    is_left_collision,
    is_up_collision,
    is_overlap,
)
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.entity import Entity
from src.hitbox import Hitbox
from src.conditional_label import ConditionalLabel
from src.dialogue import Dialogue
from src.conversation import Conversation
from src.popup import Popup
from src.popup_classes.dialogue_popup import DialoguePopup
from src.entity_classes.character import Character
from src.entity_classes.character_classes.player import Player
from src.entity_classes.character_classes.player_classes.player_wizard import PlayerWizard
from src.entity_classes.character_classes.player_classes.player_standard import PlayerStandard
from src.helpers.globals import Direction
from src.entity_classes.projectile import Projectile
from src.entity_classes.pickup_classes.wizard_pickup import Pickup
from src.entity_classes.pickup_classes.wizard_pickup import WizardPickup
from src.entity_classes.block_classes.moving_block import MovingBlock

# this is basically all of the level information, like a context
class World:
    def __init__(self, context: Context, level: list) -> None:
        # self.keys_down = {}
        # self.keys_usable = {}
        self.context = context
        self.level = level
        self.player = PlayerStandard(
            context,
            global_pos=Pair(0, 500),
        )
        self.characters = [self.player]
        self.projectiles: list[Projectile] = []
        self.moving_blocks: list[MovingBlock] = []
        self.interactables: list[Entity] = []
        self.closest_interactable: Entity = None
        self.extract_characters(self.level)
        self.moving_blocks[0].id = "101"
        self.frozen = False
        self.interaction_prompt = ConditionalLabel(self.context, text="E")
        conversation: Conversation = Conversation()
        self.popup = DialoguePopup(context, conversation.root)

    # def tick(self):
    #     self.do_physics

    def extract_characters(self, level: list):
        for x in range(len(level)):
            for y in range(len(level[x])):
                to_remove = []
                for entity in level[x][y]:
                    if issubclass(type(entity), Entity):
                        entity.tick(0, self.player.global_pos)  # first tick is necessary to set the entities' positions

                        if entity.interaction_radius:
                            self.interactables.append(entity)
                        if issubclass(type(entity), Character):
                            self.characters.append(entity)
                            to_remove.append(entity)
                        if issubclass(type(entity), MovingBlock):
                            self.moving_blocks.append(entity)
                            to_remove.append(entity)

                for entity in to_remove:
                    level[x][y].remove(entity)

    def do_physics(self, dt: float, from_loc: int, to_loc: int):
        # index = 0
        self.get_closest_interactable()
        self.check_keys()
        if self.frozen:
            for character in self.characters:
                character.update_current_sprite()
            return
        
        # self.popup.tick()
        
            
        for character in self.characters:
            if character.dead:
                character.sprites.SetAllInvisible()
                self.characters.remove(character)
                if character in self.interactables:
                    self.interactables.remove(character)
                continue
            if issubclass(type(character), Character):
                character.pre_tick(dt)  # set the character's velocity based on its movement pattern
                collisions = self.get_collisions(dt, character)

                self.process_collisions(character, collisions)
                
                # some characters don't have an attack
                if character.attack:
                    self.check_attacks(dt, character)

                # if character.dead:
                #     self.characters.remove(character)
                if character.took_damage:
                    if issubclass(type(character), Player):
                        self.freeze(1)
                        character.setFlicker(["assets/images/orange.png"], duration=character.immunity_duration_seconds, flicker_rate=0.1)
                    else:
                        character.setFlicker(["assets/images/orange.png"], duration=character.immunity_duration_seconds, flicker_rate=0.1)

                character.tick(dt, self.player.global_pos)

        self.interaction_prompt.update(self.closest_interactable)

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
        
        count = 1
        for moving_block in self.moving_blocks:
            # print(moving_block.velocity.first)
            moving_block.pre_tick(dt)
            # collisions = self.get_collisions(dt, character)
            # self.process_collisions(character, collisions)
            moving_block.tick(dt, self.player.global_pos)

        for y in range(0, len(self.level[0])):
            for x in range(from_loc, to_loc):
                for block in self.level[x][y]:
                    #continue here
                    # block = self.level[x][y]
                    if issubclass(type(block), Entity):
                        if block.dead:
                            self.level[x][y].remove(block)
                            continue
                        # collisions = self.check_collisions(block)

                        # for collision in collisions:
                        #     # self.handle_collision(block, collision.first, collision.second)
                        #     block.interact(collision.first, collision.second)

                        block.tick(dt, self.player.global_pos)

    def get_collisions(self, dt: float, entity: Entity):
        collisions = []

        entities_to_check = []
        for character in self.characters:
            entities_to_check.append(character)
        for moving_block in self.moving_blocks:
            entities_to_check.append(moving_block)

        for entity_to_check in entities_to_check:
            # if they are on the same team, they shouldn't be able to collide
            if entity_to_check == entity:
                continue
            # if abs(character.block_pos.first - entity.block_pos.first) >= entity.block_pos.first + int(entity.hitbox.width / self.block_w) + 2:
            #     continue
            # print(f"Entity: {entity.global_pos.first}, {entity.global_pos.second}")
            # print(f"Charac: {character.global_pos.first}, {character.global_pos.second}")
            if is_down_collision(dt, entity, entity_to_check):
                print("CHARACTER DOWN COLLISION")
                collisions.append(Pair(entity_to_check, Direction.DOWN))
            if is_right_collision(dt, entity, entity_to_check):
                print("CHARACTER RIGHT COLLISION")
                collisions.append(Pair(entity_to_check, Direction.RIGHT))
            if is_left_collision(dt, entity, entity_to_check):
                print("CHARACTER LEFT COLLISION")
                collisions.append(Pair(entity_to_check, Direction.LEFT))
            if is_up_collision(dt, entity, entity_to_check):
                print("CHARACTER UP COLLISION")
                collisions.append(Pair(entity_to_check, Direction.UP))
            if is_overlap(dt, entity, entity_to_check):
                if entity == self.player:
                    print("CHARACTER OVERLAP")
                collisions.append(Pair(entity_to_check, Direction.OVERLAP))

        for projectile in self.projectiles:
            if projectile == entity or (issubclass(type(entity), Projectile) and projectile.owner_id == entity.owner_id) or entity.id == projectile.owner_id:
                continue
            if is_overlap(dt, entity, projectile):
                if entity == self.player:
                    print("PROJECTILE OVERLAP")
                collisions.append(Pair(projectile, Direction.OVERLAP))

        # check below for collisions
        to_check = []
        for x in range(0, int(entity.hitbox.width / self.context.block_w) + 2):
            to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second - 1))
            to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second))

        for loc in to_check:
            for block in self.level[int(loc.first)][int(loc.second)]:
            # block = self.level[int(loc.first)][int(loc.second)]
                if issubclass(type(block), Entity):
                    if is_down_collision(dt, entity, block):
                        collisions.append(Pair(block, Direction.DOWN))

        # check right for collisions
        to_check = []
        for x in range(0, 2):
            for y in range(-1, int(entity.hitbox.height / self.context.block_w) + 1):
                to_check.append(Pair(entity.block_pos.first + int(entity.hitbox.width / self.context.block_w) + x, entity.block_pos.second + y))

        for loc in to_check:
            for block in self.level[int(loc.first)][int(loc.second)]:
                # block = self.level[int(loc.first)][int(loc.second)]
                if issubclass(type(block), Entity):
                    if is_right_collision(dt, entity, block):
                        collisions.append(Pair(block, Direction.RIGHT))

        # check left for collisions
        to_check = []
        # for x in range(-1, 1, 1):
        for y in range(-1, int(entity.hitbox.height / self.context.block_w) + 1):
            to_check.append(Pair(entity.block_pos.first - 1, entity.block_pos.second + y))

        for loc in to_check:
            for block in self.level[int(loc.first)][int(loc.second)]:
                # block = self.level[int(loc.first)][int(loc.second)]
                if issubclass(type(block), Entity):
                    if is_left_collision(dt, entity, block):
                        collisions.append(Pair(block, Direction.LEFT))

        # check up for collisions
        to_check = []
        for y in range(int(entity.hitbox.height / self.context.block_w), int(entity.hitbox.height / self.context.block_w) + 2):
            for x in range(0, int(entity.hitbox.width / self.context.block_w) + 1):
                to_check.append(Pair(entity.block_pos.first + x, entity.block_pos.second + y))

        for loc in to_check:
            for block in self.level[int(loc.first)][int(loc.second)]:
                # block = self.level[int(loc.first)][int(loc.second)]
                if issubclass(type(block), Entity):
                    if is_up_collision(dt, entity, block):
                        collisions.append(Pair(block, Direction.UP))

        # check overlap collisions
        to_check = [Pair(entity.block_pos.first, entity.block_pos.second)]

        for loc in to_check:
            for block in self.level[int(loc.first)][int(loc.second)]:
                # block = self.level[int(loc.first)][int(loc.second)]
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

            if issubclass(type(character), Player):
                if issubclass(type(collision.first), WizardPickup):
                    self.characters.remove(self.player)
                    new_player = PlayerWizard(self.context, self.player.global_pos)
                    # new_player.keys_down = self.player.keys_down
                    # new_player.keys_usable = self.player.keys_usable
                    self.player = new_player
                    self.player.update_sprite_positions(self.player.global_pos)
                    self.player.update_current_sprite()
                    self.player.setFlicker(["assets/images/sprites/goose_default/idle_right.png"], 1, 0.1)

                    # images = [pyglet.resource.image("assets/images/wizard_pickup.png"), 
                    #           pyglet.resource.image("assets/images/sprites/goose_default/idle_right.png")]
                    # ani = pyglet.image.Animation.from_image_sequence(images, duration=0.1, loop=True)
                    # sprite = pyglet.sprite.Sprite(
                    #     img=ani, batch=self.player.batch
                    # )
                    # sprite.width = self.player.sprites.current.width
                    # sprite.height = self.player.sprites.current.height
                    # sprite.x = self.player.sprites.current.x
                    # sprite.y = self.player.sprites.current.y
                    # self.player.sprites.SetVisible(sprite)
                    # self.characters.append(self.player)
                    self.characters = [self.player] + self.characters  # player should be first in the list
                    collision.first.dead = True
                    self.freeze(1)
                    # self.level[int(collision.first.block_pos.first)][int(collision.first.block_pos.second)] = None
            
            if not character.on_ground:
                character.bound = None

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
            spawn_pos.first += owner.hitbox.width + (self.context.block_w / 4)
        else:
            spawn_pos.first -= projectile.hitbox.width + (self.context.block_w / 4)
        
        new_projectile.spawn(spawn_pos, direction=owner.direction, owner_id=owner.id)
        # new_projectile.velocity.add(owner.velocity)
        self.projectiles.append(new_projectile)
    
    # def flicker(self, entity: Entity, image_filenames: list[str], duration: float, flicker_rate: float):
    #     images = []
    #     for filename in image_filenames:
    #         images.append(pyglet.resource.image(filename))
    #     # images = [pyglet.resource.image("assets/images/wizard_pickup.png"), 
    #     #             pyglet.resource.image("assets/images/sprites/goose_default/idle_right.png")]
    #     ani = pyglet.image.Animation.from_image_sequence(images, duration=flicker_rate, loop=True)
    #     sprite = pyglet.sprite.Sprite(
    #         img=ani, batch=self.player.batch
    #     )
    #     sprite.width = self.player.sprites.current.width
    #     sprite.height = self.player.sprites.current.height
    #     sprite.x = self.player.sprites.current.x
    #     sprite.y = self.player.sprites.current.y
    #     self.player.sprites.SetVisible(sprite)
    
    def freeze(self, duration: float):
        print(f"FREEZING FOR {duration} SECONDS")
        self.frozen = True
        pyglet.clock.schedule_once(self.unfreeze, duration)

    def unfreeze(self, dt):
        self.frozen = False
    
    def get_closest_interactable(self):
        smallest_dist = sys.maxsize
        closest = None
        for entity in self.interactables:
            dist = hb_distance(self.player.hitbox, entity.hitbox)
            # print(entity.interaction_radius)
            # print(dist)
            if dist <= entity.interaction_radius and dist < smallest_dist:
                smallest_dist = dist
                closest = entity
        
        self.closest_interactable = closest
                

    def check_keys(self):
        # print(pyglet.window.key._1)
        # print(self.context.keys_usable.get(pyglet.window.key._1, False))
        if self.context.keys_down.get(pyglet.window.key._1, False) and self.context.keys_usable.get(pyglet.window.key._1, False):
            self.context.keys_usable[pyglet.window.key._1] = False
            self.popup.handle_key_press(pyglet.window.key._1)
        elif not self.context.keys_down.get(pyglet.window.key._1, False):
            self.context.keys_usable[pyglet.window.key._1] = True
        if self.context.keys_down.get(pyglet.window.key._2, False) and self.context.keys_usable.get(pyglet.window.key._2, False):
            self.context.keys_usable[pyglet.window.key._2] = False
            self.popup.handle_key_press(pyglet.window.key._2)
        elif not self.context.keys_down.get(pyglet.window.key._2, False):
            self.context.keys_usable[pyglet.window.key._2] = True
        if self.context.keys_down.get(pyglet.window.key._3, False) and self.context.keys_usable.get(pyglet.window.key._3, False):
            self.context.keys_usable[pyglet.window.key._3] = False
            self.popup.handle_key_press(pyglet.window.key._3)
        elif not self.context.keys_down.get(pyglet.window.key._3, False):
            self.context.keys_usable[pyglet.window.key._3] = True
        if self.context.keys_down.get(pyglet.window.key._4, False) and self.context.keys_usable.get(pyglet.window.key._4, False):
            self.context.keys_usable[pyglet.window.key._4] = False
            self.popup.handle_key_press(pyglet.window.key._4)
        elif not self.context.keys_down.get(pyglet.window.key._4, False):
            self.context.keys_usable[pyglet.window.key._4] = True
        if self.context.keys_down.get(pyglet.window.key.Q, False) and self.context.keys_usable.get(pyglet.window.key.Q, False):
            self.context.keys_usable[pyglet.window.key.Q] = False
            if self.popup.active:
                print("in here")
                self.popup.deactivate()
                self.frozen = False
        elif not self.context.keys_down.get(pyglet.window.key.Q, False):
            self.context.keys_usable[pyglet.window.key.Q] = True
        if self.context.keys_down.get(pyglet.window.key.E, False) and self.context.keys_usable.get(pyglet.window.key.E, False):
            self.context.keys_usable[pyglet.window.key.E] = False
            if self.closest_interactable:
                print("&& INTERACTION GOES HERE")
                self.popup.activate()
                self.frozen = True
                # self.closest_interactable.dead = True
            # for entity in self.interactables:
            #     if hb_distance(self.player.hitbox, entity.hitbox) <= entity.interaction_radius:
            #         print("&& INTERACTION GOES HERE")
            #         entity.dead = True

            #         ########################################################################
            #         # TODO: figure out a way to indicate that you are in interaction range #
            #         ########################################################################
        elif not self.context.keys_down.get(pyglet.window.key.E, False):
            self.context.keys_usable[pyglet.window.key.E] = True
            # self.direction = Direction.LEFT
        if self.context.keys_down.get(pyglet.window.key.T, False):
            self.popup.activate()
            self.frozen = True


    # def handle_key_press(self, symbol, modifiers):
    #     # print(f"* pressing key {symbol}")
    #     self.keys_down[symbol] = True
    #     # self.player.handle_key_press(symbol, modifiers)

    # def handle_key_release(self, symbol, modifiers):
    #     # print(f"^ releasing key {symbol}")
    #     self.keys_down[symbol] = False
    #     # self.player.handle_key_release(symbol, modifiers)