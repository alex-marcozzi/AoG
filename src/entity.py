import pyglet
from src.helpers.interfaces import Pair
from src.helpers.context import Context
from src.helpers.utils import block_width, std_speed, make_sprite
from src.helpers.globals import Direction
from src.hitbox import Hitbox
from src.sprite_collection import SpriteCollection
import uuid

# loaded_images = {}  # key: filename, value: image


class Entity:
    def __init__(
        self,
        context: Context,
        sprites: SpriteCollection,
        global_pos: Pair,
        hitbox_width: float,
        hitbox_height: float,
        velocity=None,
        acceleration=None,
    ):
        self.context = context
        self.sprites = sprites
        self.hitbox = Hitbox(pos=global_pos, width=hitbox_width, height=hitbox_height)
        self.global_pos = global_pos.copy()
        self.block_pos = Pair(
            self.global_pos.first // self.context.block_w,
            (self.global_pos.second + 10) // self.context.block_w,
        )
        self.velocity = velocity if velocity else Pair(0, 0)
        self.acceleration = acceleration if acceleration else Pair(0, 0)
        self.modifiers = ["collidable"]
        self.direction = Direction.RIGHT
        self.id = uuid.uuid1()
        self.dead = False
        self.flickering = False
        self.flicker_flag = False
        self.flicker_filename = ""
        self.flicker_sprite = None
        self.prev_dt = 0

    def copy(self):
        new_copy = Entity(
            context=self.context,
            sprites=self.sprites.copy(),
            global_pos=self.global_pos,
            sprite_width=self.sprites.idle_right.width,
            sprite_height=self.sprites.idle_right.height,
            hitbox_width=self.hitbox.width,
            hitbox_height=self.hitbox.height,
            velocity=self.velocity,
            acceleration=self.acceleration,
        )
        return new_copy

    def tick_pos_only(self, dt: float):
        # if self.id == "999":
        #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #     print(self.velocity.first)
        #     print(self.velocity.first * dt)
        #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        self.global_pos.add(Pair(self.velocity.first * dt, self.velocity.second * dt))
        # self.velocity.add(self.acceleration)

    def tick(self, dt: float, camera_pos: Pair):
        self.global_pos.add(Pair(self.velocity.first * dt, self.velocity.second * dt))
        self.velocity.add(Pair(self.acceleration.first * dt, self.acceleration.second * dt))
        # self.global_pos.add

        # camera_pos == player.global_pos (middle of screen)
        # if self.sprites:
        #     self.sprites.idle_right.x = self.global_pos.first - (
        #         camera_pos.first - (self.window.width / 2)
        #     )
        #     self.sprites.idle_right.x = self.global_pos.second - (
        #         camera_pos.second - (self.window.height / 2)
        #     )
        self.block_pos = Pair(
            self.global_pos.first // self.context.block_w,
            (self.global_pos.second + 10) // self.context.block_w,
        )
        self.hitbox.pos = self.global_pos.copy()

        self.update_sprite_positions(camera_pos)
        self.update_current_sprite()
        self.prev_dt = dt

    # def draw(self):
    #     self.sprite.draw()

    def update_sprite_positions(self, camera_pos: Pair):
        self.sprites.idle_right.x = self.global_pos.first - (
            camera_pos.first - (self.context.window.width / 2) - ((self.hitbox.width - self.sprites.idle_right.width) / 2)
        )
        self.sprites.idle_right.y = self.global_pos.second - (
            camera_pos.second - (self.context.window.height / 2)
        )
        self.sprites.idle_left.x = self.sprites.idle_right.x
        self.sprites.idle_left.y = self.sprites.idle_right.y
        
        if self.sprites.slow_move_right:
            self.sprites.slow_move_right.x = self.sprites.idle_right.x
            self.sprites.slow_move_right.y = self.sprites.idle_right.y
        
        if self.sprites.slow_move_left:
            self.sprites.slow_move_left.x = self.sprites.idle_right.x
            self.sprites.slow_move_left.y = self.sprites.idle_right.y
        
        if self.sprites.fast_move_right:
            self.sprites.fast_move_right.x = self.sprites.idle_right.x
            self.sprites.fast_move_right.y = self.sprites.idle_right.y
        
        if self.sprites.fast_move_left:
            self.sprites.fast_move_left.x = self.sprites.idle_right.x
            self.sprites.fast_move_left.y = self.sprites.idle_right.y
        
        # if self.sprites.attack_right:
        #     self.sprites.attack_right.x = self.sprites.idle_right.x
        #     self.sprites.attack_right.y = self.sprites.idle_right.y
        
        # if self.sprites.attack_left:
        #     self.sprites.attack_left.x = self.sprites.idle_right.x - self.attack.range
        #     self.sprites.attack_left.y = self.sprites.idle_right.y
        
        if self.sprites.damaged_right:
            self.sprites.damaged_right.x = self.sprites.idle_right.x
            self.sprites.damaged_right.y = self.sprites.idle_right.y
        
        if self.sprites.damaged_left:
            self.sprites.damaged_left.x = self.sprites.idle_right.x
            self.sprites.damaged_left.y = self.sprites.idle_right.y
            
        if self.flickering:
            self.flicker_sprite.x = self.sprites.idle_right.x
            self.flicker_sprite.y = self.sprites.idle_right.y
    
    def update_current_sprite(self):
        if self.flickering and self.flicker_flag:
            self.sprites.SetVisible(self.flicker_sprite)
            self.flicker_flag = False
        else:
            if self.direction == Direction.RIGHT:
                self.sprites.SetVisible(self.sprites.idle_right)
            elif self.direction == Direction.LEFT:
                self.sprites.SetVisible(self.sprites.idle_left)
            self.sprites.SetVisible(self.sprites.idle_right)
            self.flicker_flag = True


    def interact(self, entity: "Entity", direction):
        if "collidable" in entity.modifiers:
            self.interact_collidable(entity, direction)

        pass

    def interact_collidable(self, entity: "Entity", direction):
        pass

    def nextPos(self):
        return Pair(
            self.global_pos.first + self.velocity.first,
            self.global_pos.second + self.velocity.second,
        )

    def bottomLeft(self):
        return self.global_pos

    def bottomRight(self):
        return Pair(self.global_pos.first + self.hitbox.width, self.global_pos.second)

    def topLeft(self):
        return Pair(self.global_pos.first, self.global_pos.second + self.hitbox.height)

    def topRight(self):
        return Pair(
            self.global_pos.first + self.hitbox.width,
            self.global_pos.second + self.hitbox.height,
        )
    
    def setFlicker(self, image_filenames: list[str], duration: float, flicker_rate: float):
        # images = [pyglet.resource.image(self.flicker_filename)]
        # for filename in image_filenames:
        #     images.append(pyglet.resource.image(filename))
        
        # ani = pyglet.image.Animation.from_image_sequence(images, duration=flicker_rate, loop=True)
        sprite = pyglet.sprite.Sprite(
            img=pyglet.resource.image(image_filenames[0]), batch=self.context.batch
        )
        sprite.width = self.sprites.current.width
        sprite.height = self.sprites.current.height
        sprite.x = self.sprites.current.x
        sprite.y = self.sprites.current.y
        sprite.visible = False
        # self.sprites.SetVisible(sprite)
        self.flicker_sprite = sprite
        self.flickering = True
        self.flicker_flag = True

        pyglet.clock.schedule_once(self.unsetFlicker, duration)
    
    def unsetFlicker(self, dt):
        self.flickering = False
