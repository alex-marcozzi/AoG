# import pyglet
# from src.helpers.utils import is_down_collision, is_right_collision, block_width, std_speed, gravity
# from src.helpers.interfaces import Pair
# from src.entity import Entity
# from src.helpers.globals import Direction

# # this is basically all of the level information, like a context
# class World:
#     def __init__(self, window: pyglet.window.Window, level: list) -> None:
#         self.window = window
#         self.block_w = block_width(window)
#         self.standard_speed = std_speed(window)
#         self.level = level
#         # self.player = Entity(window,
#         #                      "assets/images/goose.png",
#         #                      global_pos=Pair(0, 200),
#         #                      velocity=Pair(0, 0),
#         #                      acceleration=Pair(0, gravity(window)),
#         #                      width=self.block_w,
#         #                      height=self.block_w * 2)
    
#     # def do_physics(from_loc: int, to_loc: int):



#     def check_collisions(self, entity: Entity, entity_block_pos: Pair):
#         # player_block_pos = Pair(self.player.global_pos.first // self.block_w, self.player.global_pos.second // block_h)

#         # the three squares below the entity
#         to_check = [Pair(entity_block_pos.first - 1, entity_block_pos.second - 1),  # behind and below
#                     Pair(entity_block_pos.first, entity_block_pos.second - 1),  # straight below
#                     Pair(entity_block_pos.first + 1, entity_block_pos.second - 1)]  # infront and below
        
#         for loc in to_check:
#             block = self.level[int(loc.first)][int(loc.second)]
#             if type(block) is Entity:
#                 next_player_pos = Pair(self.player.global_pos.first, self.player.global_pos.second + self.player.velocity.second)
#                 if is_down_collision(next_player_pos, block.global_pos, self.block_w):
#                     return Direction.DOWN
#                 if is_right_collision(next_player_pos, block.global_pos, self.block_w):
#                     return Direction.RIGHT