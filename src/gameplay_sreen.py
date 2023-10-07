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
        self.batch = pyglet.graphics.Batch()

        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        # self.level = build_level1(window)
        # self.player = Player(window,
        #                      "assets/images/goose.png",
        #                      global_pos=Pair(0, 500),
        #                      velocity=Pair(0, 0),
        #                      acceleration=Pair(0, gravity(window)),
        #                      width=self.block_w,
        #                      height=self.block_w * 2,
        #                      batch=self.batch)
        self.world = World(window, build_level1(window, self.batch), self.batch)
        self.loaded_indexes = Pair(int(0), int(30))
        self.background = pyglet.sprite.Sprite(pyglet.image.load('assets/images/background.png'))
        # self.keys_down = {}
        # self.keys_usable = {}
    
    def tick(self):

        # self.player.velocity = Pair(0, self.player.velocity.second)
        # self.check_keys()
        # self.player.check_keys()
        

        # self.handle_collisions()
        self.loaded_indexes = Pair(max(0, int(self.world.player.block_pos.first - 12)), min(len(self.world.level), int(self.world.player.block_pos.first + 12)))

        self.world.do_physics(self.loaded_indexes.first, self.loaded_indexes.second)

    def draw(self):
        self.background.draw()
        # for character in self.world.characters:
        #     if abs(character.block_pos.first - self.player.block_pos.first) < 12:
        #         character.draw()
        # self.player.draw()
        # for x in range(self.loaded_indexes.first, self.loaded_indexes.second):
        #     for y in range(len(self.world.level[0])):
        #         if issubclass(type(self.world.level[x][y]), Entity):
        #             self.world.level[x][y].draw()
        self.batch.draw()
        
        label = pyglet.text.Label(str(self.world.player.hp),
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.block_w * 3, y=self.window.height - self.block_w,
                          anchor_x='center', anchor_y='center')
        label.draw()
        
        pass

    def handle_key_press(self, symbol, modifiers):
        print(f"* pressing key {symbol}")
        self.world.player.handle_key_press(symbol, modifiers)

    def handle_key_release(self, symbol, modifiers):
        print(f"^ releasing key {symbol}")
        self.world.player.handle_key_release(symbol, modifiers)

    
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