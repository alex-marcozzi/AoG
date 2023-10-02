import pyglet
from src.helpers.level_builders import build_level1
from src.helpers.utils import block_width, std_speed, gravity
from src.helpers.physics import is_down_collision, is_up_collision, is_right_collision, is_left_collision
from src.helpers.interfaces import Pair
from src.entity import Entity
from src.entity_classes.player import Player
from src.world import World

class GameplayScreen:
    def __init__(self, window: pyglet.window.Window):
        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        self.level = build_level1(window)
        self.player = Player(window,
                             "assets/images/goose.png",
                             global_pos=Pair(0, 500),
                             velocity=Pair(0, 0),
                             acceleration=Pair(0, gravity(window)),
                             width=self.block_w,
                             height=self.block_w * 2)
        self.world = World(window, build_level1(window), self.player)
        self.loaded_indexes = Pair(int(0), int(30))
        # self.keys_down = {}
        # self.keys_usable = {}
    
    def tick(self):

        self.player.velocity = Pair(0, self.player.velocity.second)
        # self.check_keys()
        self.player.check_keys()
        

        # self.handle_collisions()
        self.loaded_indexes = Pair(max(0, int(self.player.block_pos.first - 12)), min(len(self.world.level), int(self.player.block_pos.first + 12)))

        self.world.do_physics(self.loaded_indexes.first, self.loaded_indexes.second)
        # self.player.tick(self.player.global_pos)
        # player_block_pos = Pair(self.player.global_pos.first / self.block_w, self.player.global_pos.second / self.block_w)

        # for x in range(self.loaded_indexes.first, self.loaded_indexes.second):
        #     for y in range(len(self.level[0])):
        #         if type(self.level[x][y]) is Entity:
        #             self.level[x][y].tick(self.player.global_pos)

    def draw(self):
        for character in self.world.characters:
            if abs(character.block_pos.first - self.player.block_pos.first) < 12:
                character.draw()
        # self.player.draw()
        for x in range(self.loaded_indexes.first, self.loaded_indexes.second):
            for y in range(len(self.world.level[0])):
                # if type(self.world.level[x][y]) is Entity:
                if issubclass(type(self.world.level[x][y]), Entity):
                    self.world.level[x][y].draw()
        
        label = pyglet.text.Label(str(self.world.player.hp),
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.block_w * 3, y=self.window.height - self.block_w,
                          anchor_x='center', anchor_y='center')
        label.draw()
        
        pass

    def handle_key_press(self, symbol, modifiers):
        print(f"* pressing key {symbol}")
        self.player.handle_key_press(symbol, modifiers)
        # self.keys_down[symbol] = True

    def handle_key_release(self, symbol, modifiers):
        print(f"^ releasing key {symbol}")
        self.player.handle_key_release(symbol, modifiers)
        # self.keys_down[symbol] = False

    # def handle_collisions(self):
    #     block_w = block_h = self.window.width / 15
    #     player_block_pos = Pair(self.player.global_pos.first // self.block_w, self.player.global_pos.second // self.block_w)

    #     # the three squares below the player
    #     to_check = [
    #                 # Pair(player_block_pos.first - 1, player_block_pos.second),  # behind and below
    #                 Pair(player_block_pos.first, player_block_pos.second),  # straight below
    #                 Pair(player_block_pos.first + 1, player_block_pos.second),
    #                 # Pair(player_block_pos.first - 1, player_block_pos.second - 1),  # behind and below
    #                 Pair(player_block_pos.first, player_block_pos.second - 1),  # straight below
    #                 Pair(player_block_pos.first + 1, player_block_pos.second - 1),
    #                 # Pair(player_block_pos.first - 1, player_block_pos.second - 2),  # behind and below
    #                 Pair(player_block_pos.first, player_block_pos.second - 2),  # straight below
    #                 Pair(player_block_pos.first + 1, player_block_pos.second - 2),
    #                 # Pair(player_block_pos.first - 1, player_block_pos.second + 1),  # behind and below
    #                 Pair(player_block_pos.first, player_block_pos.second + 1),  # straight below
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 1),
    #                 # Pair(player_block_pos.first - 1, player_block_pos.second),  # behind and below
    #                 # Pair(player_block_pos.first, player_block_pos.second),  # straight below
    #                 # Pair(player_block_pos.first + 1, player_block_pos.second),  # infront and below
    #                 ]
        
        
    #     for loc in to_check:
    #         block = self.level[int(loc.first)][int(loc.second)]
    #         if type(block) is Entity and "collidable" in block.modifiers:
    #             if is_down_collision(self.player, block):
    #                 self.player.global_pos = Pair(self.player.global_pos.first, block.global_pos.second + block.sprite.height)
    #                 self.player.velocity = Pair(self.player.velocity.first, 0)
    #                 self.keys_usable[pyglet.window.key.SPACE] = True
    #                 print("! DOWN COLLISION")
        
    #     to_check = [Pair(player_block_pos.first + 1, player_block_pos.second),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 3),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second - 1),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second - 2),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second - 3)
    #                 ]
        
    #     for loc in to_check:
    #         block = self.level[int(loc.first)][int(loc.second)]
    #         if type(block) is Entity and "collidable" in block.modifiers:
    #             if is_right_collision(self.player, block):
    #                 self.player.global_pos = Pair(block.global_pos.first - self.player.sprite.width, self.player.global_pos.second)
    #                 self.player.velocity = Pair(0, self.player.velocity.second)
    #                 print("! RIGHT COLLISION")
        
    #     to_check = [
    #                 Pair(player_block_pos.first, player_block_pos.second - 1),
    #                 Pair(player_block_pos.first, player_block_pos.second),
    #                 Pair(player_block_pos.first, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first, player_block_pos.second + 3),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second - 1),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 3),
    #                 ]
        
    #     for loc in to_check:
    #         block = self.level[int(loc.first)][int(loc.second)]
    #         if type(block) is Entity and "collidable" in block.modifiers:
    #             if is_left_collision(self.player, block):
    #                 print("! LEFT COLLISION")
    #                 self.player.global_pos = Pair(block.global_pos.first + block.sprite.width, self.player.global_pos.second)
    #                 self.player.velocity = Pair(0, self.player.velocity.second)
        

    #     # the three squares below the player
    #     to_check = [
    #                 Pair(player_block_pos.first - 1, player_block_pos.second),
    #                 Pair(player_block_pos.first, player_block_pos.second),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 1),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 2),
    #                 Pair(player_block_pos.first - 1, player_block_pos.second + 3),
    #                 Pair(player_block_pos.first, player_block_pos.second + 3),
    #                 Pair(player_block_pos.first + 1, player_block_pos.second + 3),
    #                 ]
        
    #     for loc in to_check:
    #         block = self.level[int(loc.first)][int(loc.second)]
    #         if type(block) is Entity and "collidable" in block.modifiers:
    #             if is_up_collision(self.player, block):
    #                 print("! UP COLLISION")
    #                 self.player.global_pos = Pair(self.player.global_pos.first, block.global_pos.second - self.player.sprite.height)
    #                 self.player.velocity = Pair(self.player.velocity.first, 0)
    
    # def check_keys(self):
    #     if self.keys_down.get(pyglet.window.key.A, False):
    #         self.player.velocity = Pair(self.player.velocity.first - self.standard_speed, self.player.velocity.second)
    #     if self.keys_down.get(pyglet.window.key.D, False):
    #         self.player.velocity = Pair(self.player.velocity.first + self.standard_speed, self.player.velocity.second)
    #     if self.keys_down.get(pyglet.window.key.SPACE, False) and self.keys_usable.get(pyglet.window.key.SPACE, True):
    #         self.player.velocity = Pair(self.player.velocity.first, self.player.velocity.second + (self.block_w / 5))
    #         # self.keys_usable[pyglet.window.key.SPACE] = False


        # if self.keys_down.get(pyglet.window.key.A, False):
        #     self.player.velocity = (self.player.velocity[0] - (self.block_w / 8), self.player.velocity[1])
        # if self.keys_down.get(pyglet.window.key.D, False):
        #     self.player.velocity = (self.player.velocity[0] + (self.block_w / 8), self.player.velocity[1])
        # if self.keys_down.get(pyglet.window.key.SPACE, False) and self.keys_usable[pyglet.window.key.SPACE]:
        #     self.player.velocity = (self.player.velocity[0], self.player.velocity[1] + (self.block_w / 5))
        #     self.keys_usable[pyglet.window.key.SPACE] = False

        # BELOW: has accelleration physics, now that I think about it we could just set the acceleration
        # if not (self.keys_down.get(pyglet.window.key.A, False) or self.keys_down.get(pyglet.window.key.D, False)):
        #     self.player.velocity = (max(self.player.velocity[0] - 3, 0), self.player.velocity[1])
        # if self.keys_down.get(pyglet.window.key.A, False):
        #     self.player.velocity = (max(self.player.velocity[0] - 1, -1 * (self.block_w / 8)), self.player.velocity[1])
        # if self.keys_down.get(pyglet.window.key.D, False):
        #     self.player.velocity = (min(self.player.velocity[0] + 1, self.block_w / 8), self.player.velocity[1])
        # if self.keys_down.get(pyglet.window.key.SPACE, False) and self.keys_usable[pyglet.window.key.SPACE]:
        #     self.player.velocity = (self.player.velocity[0], self.player.velocity[1] + (self.block_w / 5))
        #     self.keys_usable[pyglet.window.key.SPACE] = False

    
    # TODO:
    #   X0. make a "globals" file where you define our constants, like block_width, speed ratios (have a normalized system), etc.
    #   X00. use the globals file to make movement independent of screen size and framerate, it should always display the same
    #   4.55 make a *World* class that gets passed around and contains the level map.
    #           - it could have a tick function
    #           - it could check if blocks are coliding and return which direction they are
    #           - this direction could be passed to the Entity class's "interact" function, which could be super readable
    #           - imagine this: 
    #               Entity1.interact(Entity2, dir="right"):
    #                   if dir == "right":
    #                       if "dangerous" in Entity2.modifiers:
    #                           Entity1.take_damage()
    #                       elif "collidable" in Entity2.modifiers:
    #                           Entity1.global_pos = Pair(Entity2.global_pos.first - block_w, Entity1.second)
    #                   etc.
    #   1. add side and top collisions
    #   2. add handling for when you fall (catch exception or just check if loadable)
    #   3. create other types of entities, every used object should be a subclass of Entity, never use Entity directly. 
    #      we should have a new class that inherits from Entity for each of the following:
    #        - character (then have another subclass for player and enemy, then enemy can have another subclass for each enemy type)
    #        - block (modifiers: collidable)
    #        - moving block (modifiers: collidable) (you can use math to make these move how you want, different formulas to affect acceleration, for example, acceleration deceases the farther away from the anchor point)
    #        - spike block (modifiers: collidable, deadly)
    #        - player
    #        - enemy (modifiers: deadly)
    #   4. add mechanics, like double jump, glide, 
    #   5. make menus work (make other screen classes and integrate the gameplay_screen fully with the rest of the engine)