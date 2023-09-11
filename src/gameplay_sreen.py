import pyglet
from src.helpers.level_builders import build_level1
from src.helpers.utils import is_down_collision, block_width, std_speed, gravity
from src.entity import Entity

class GameplayScreen:
    def __init__(self, window: pyglet.window.Window):
        self.window = window
        self.block_w = block_width(window)
        self.standard_speed = std_speed(window)
        self.level = build_level1(window)
        self.player = Entity(window,
                             "assets/images/orange.png",
                             global_pos=(0, 200),
                             velocity=(0, 0),
                             acceleration=(0, gravity(window)),
                             width=self.block_w,
                             height = self.block_w * 2)
        self.loaded_indexes = [int(0), int(30)]
        self.keys_down = {}
        self.keys_usable = {}
    
    def tick(self):
        self.player.velocity = (0, self.player.velocity[1])
        
        self.check_keys()

        self.handle_collisions()

        self.player.tick(self.player.global_pos)
        player_block_pos = (self.player.global_pos[0] / self.block_w, self.player.global_pos[1] / self.block_w)
        self.loaded_indexes = (int(player_block_pos[0] - 12), int(player_block_pos[0] + 12))

        # print(self.loaded_indexes)
        for x in range(self.loaded_indexes[0], self.loaded_indexes[1]):
            for y in range(len(self.level[0])):
                if type(self.level[x][y]) is Entity:
                    self.level[x][y].tick(self.player.global_pos)

    def draw(self):
        self.player.draw()
        for x in range(self.loaded_indexes[0], self.loaded_indexes[1]):
            for y in range(len(self.level[0])):
                if type(self.level[x][y]) is Entity:
                    self.level[x][y].draw()
        pass

    def handle_key_press(self, symbol, modifiers):
        print(f"* pressing key {symbol}")
        self.keys_down[symbol] = True

    def handle_key_release(self, symbol, modifiers):
        print(f"^ releasing key {symbol}")
        self.keys_down[symbol] = False

    def handle_collisions(self):
        block_w = block_h = self.window.width / 15
        player_block_pos = (self.player.global_pos[0] // block_w, self.player.global_pos[1] // block_h)
        to_check = [(player_block_pos[0] - 1, player_block_pos[1] - 1), (player_block_pos[0], player_block_pos[1] - 1),(player_block_pos[0] + 1, player_block_pos[1] - 1),]
        for loc in to_check:
            block = self.level[int(loc[0])][int(loc[1])]
            if type(block) is Entity and "collidable" in block.modifiers:
                print(f"{loc} is an entity")
                print(f"{self.player.global_pos}, {block.global_pos[1] + block_w}")
                next_player_pos = (self.player.global_pos[0], self.player.global_pos[1] + self.player.velocity[1])
                if is_down_collision(next_player_pos, block.global_pos, block_w):
                    print("GETTING CAUGHT***************")
                    self.player.global_pos = (self.player.global_pos[0], block.global_pos[1] + block_w)
                    self.player.velocity = (self.player.velocity[0], 0)
                    self.keys_usable[pyglet.window.key.SPACE] = True
    
    def check_keys(self):
        if self.keys_down.get(pyglet.window.key.A, False):
            self.player.velocity = (self.player.velocity[0] - self.standard_speed, self.player.velocity[1])
        if self.keys_down.get(pyglet.window.key.D, False):
            self.player.velocity = (self.player.velocity[0] + self.standard_speed, self.player.velocity[1])
        if self.keys_down.get(pyglet.window.key.SPACE, False) and self.keys_usable[pyglet.window.key.SPACE]:
            self.player.velocity = (self.player.velocity[0], self.player.velocity[1] + (self.block_w / 5))
            self.keys_usable[pyglet.window.key.SPACE] = False


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
    #   0. make a "globals" file where you define our constants, like block_width, speed ratios (have a normalized system), etc.
    #   00. use the globals file to make movement independent of screen size and framerate, it should always display the same
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