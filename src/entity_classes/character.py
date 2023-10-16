import pyglet
from src.helpers.utils import std_speed, block_width, make_sprite
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.attack import Attack
from src.sprite_collection import SpriteCollection
from src.helpers.globals import Direction
import time

class Character(Entity):
    def __init__(
        self,
        window,
        sprites: SpriteCollection,
        global_pos: Pair,
        velocity: Pair,
        acceleration: Pair,
        # sprite_width: float,
        # sprite_height: float,
        hitbox_width: float,
        hitbox_height: float,
        batch,
        hp: int,
        attack: Attack = None,
    ):
        self.sprites = sprites
        self.sprites.SetVisible(self.sprites.idle_right)
        
        super().__init__(
            window,
            sprites,
            global_pos,
            velocity,
            acceleration,
            None,
            None,
            hitbox_width,
            hitbox_height,
            batch,
        )

        self.hp = hp
        self.width_in_blocks = hitbox_width // block_width(window)
        # self.standard_speed = std_speed(window)
        # self.block_below = None
        self.on_ground = False
        self.immunity_start = time.time()
        self.immunity_duration_seconds = 1
        self.attack = attack
        self.direction = Direction.RIGHT

        # self.sprites = [self.sprite,
        #                 make_sprite(sprite_filename=)
        #                 ]

        # pyglet.sprite.Sprite(
        #     img=loaded_images[sprite_filename], batch=batch
        # )
        
        # self.attack_sprite_filename = attack_sprite_filename
        # if attack_sprite_filename:
        #     if not attack_sprite_filename in loaded_images.keys():
        #         loaded_images[attack_sprite_filename] = pyglet.resource.image(attack_sprite_filename)
        #     self.attack_sprite = pyglet.sprite.Sprite(
        #         img=loaded_images[attack_sprite_filename], batch=batch
        #     )
        #     self.attack_sprite.width = self.attack.hitboxes[0].width
        #     self.attack_sprite.height = self.attack.hitboxes[0].height
        #     self.attack_sprite.visible = False

    def copy(self):
        new_copy = Character(window=self.window,
                             sprites=self.sprites.copy(),
                             global_pos=self.global_pos,
                             velocity=self.velocity,
                             acceleration=self.acceleration,
                             hitbox_width=self.hitbox.width,
                             hitbox_height=self.hitbox.height,
                             batch=self.batch,
                             hp=self.hp,
                             attack=self.attack)
        
        return new_copy
        # (
        #     window=self.window,
        #     sprite_filename=self.sprite_filename,
        #     global_pos=self.global_pos,
        #     velocity=self.velocity,
        #     acceleration=self.acceleration,
        #     sprite_width=self.sprite.width,
        #     sprite_height=self.sprite.height,
        #     hitbox_width=self.hitbox.width,
        #     hitbox_height=self.hitbox.height,
        #     batch=self.batch,
        # )
        # return new_copy

    def pre_tick(self, dt: float):
        self.velocity = Pair(0, self.velocity.second)
        # self.check_keys()
        # self.player.check_keys()

    def tick(self, dt: float, camera_pos: Pair):
        super().tick(dt, camera_pos)

        self.update_sprite_positions(camera_pos)

        self.update_current_sprite()
        # if self.attack:
        #     if self.attack.inProgress():
        #         if self.direction == Direction.RIGHT:
        #             self.sprites.SetVisible(self.sprites.attack_right)
        #         elif self.direction == Direction.LEFT:
        #             self.sprites.SetVisible(self.sprites.attack_left)
        #     else:
        #         if self.direction == Direction.RIGHT:
        #             self.sprites.SetVisible(self.sprites.idle_right)
        #         elif self.direction == Direction.LEFT:
        #             self.sprites.SetVisible(self.sprites.idle_left)
        #             # self.sprite.visible = True
        #             # self.attack_sprite.visible = False

        

        if self.hp <= 0:
            return False

        return True
    
    # def draw(self):
    #     if self.attack and self.attack.inProgress():
    #         self.attack_sprite.draw()
    #     else:
    #         super().draw()

    def update_sprite_positions(self, camera_pos: Pair):
        super().update_sprite_positions(camera_pos)
        if self.sprites.attack_right:
            self.sprites.attack_right.x = self.sprites.idle_right.x
            self.sprites.attack_right.y = self.sprites.idle_right.y
        
        if self.sprites.attack_left:
            self.sprites.attack_left.x = self.sprites.idle_right.x - self.attack.range
            self.sprites.attack_left.y = self.sprites.idle_right.y
    
    def update_current_sprite(self):
        if self.attack:
            if self.attack.inProgress():
                if self.direction == Direction.RIGHT:
                    self.sprites.SetVisible(self.sprites.attack_right)
                elif self.direction == Direction.LEFT:
                    self.sprites.SetVisible(self.sprites.attack_left)
            else:
                if self.direction == Direction.RIGHT:
                    self.sprites.SetVisible(self.sprites.idle_right)
                elif self.direction == Direction.LEFT:
                    self.sprites.SetVisible(self.sprites.idle_left)
                    # self.sprite.visible = True
                    # self.attack_sprite.visible = False

    def interact(self, entity: Entity, direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)

    def interact_collidable(self, entity: Entity, direction):
        if direction == Direction.DOWN:
            self.global_pos = Pair(
                self.global_pos.first, entity.global_pos.second + entity.hitbox.height
            )
            self.velocity = Pair(self.velocity.first + entity.velocity.first, 0)
        #     self.on_ground = True
        # else:
        #     self.on_ground = False
        if direction == Direction.RIGHT:
            if (
                not issubclass(type(entity), Character)
                and self.block_pos.second - 1 == entity.block_pos.second
            ):
                return
            print("! RIGHT COLLISION")
            self.global_pos = Pair(
                entity.hitbox.pos.first - self.hitbox.width, self.global_pos.second
            )
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.LEFT:
            if (
                not issubclass(type(entity), Character)
                and self.block_pos.second - 1 == entity.block_pos.second
            ):
                return
            print("! LEFT COLLISION")
            self.global_pos = Pair(
                entity.global_pos.first + entity.hitbox.width, self.global_pos.second
            )
            self.velocity = Pair(0, self.velocity.second)
        if direction == Direction.UP:
            print("! UP COLLISION")
            self.global_pos = Pair(
                self.global_pos.first, entity.hitbox.pos.second - self.hitbox.height
            )
            self.velocity = Pair(self.velocity.first, 0)

    def interact_dangerous(self, entity: Entity, direction):
        self.takeDamage(1)

    def takeDamage(self, amount):
        now = time.time()
        if (now - self.immunity_start > self.immunity_duration_seconds):
            self.hp = max(self.hp - amount, 0)
            self.immunity_start = time.time()  # epoch time

    def takeHit(self, attack: Attack):
        # when we add modifiers later we could do checking here:
        # if "poisonous" in self.modifiers:
        #       etc.

        self.takeDamage(amount=attack.damage)

    # # sprite_data:
    # #       key: filename
    # #       value: Pair(width, height)
    # def initializeSprites(self, sprite_data: dict):
    #     for filename, sizing in sprite_data:
            