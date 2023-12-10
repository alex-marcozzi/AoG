import pyglet
from src.helpers.utils import make_sprite
from src.helpers.context import Context
class Popup:
    def __init__(self, context: Context, background_sprite_filename: str, percent_width, percent_height):
        self.context = context
        self.percent_width = percent_width
        self.percent_height = percent_height

        self.background_sprite: pyglet.sprite.Sprite = make_sprite(
            sprite_filename=background_sprite_filename,
            width=context.window.width * percent_width,
            height=context.window.height * percent_height,
            visible=False,
            batch=context.batch)
        self.background_sprite.x = context.window.width * ((1 - percent_width) / 2)
        self.background_sprite.y = context.window.height * ((1 - percent_height) / 2)
        self.background_sprite.z = 2
        # self.background_sprite.visible = False
        self.active = False
    
    def activate(self):
        self.active = True
        self.background_sprite.visible = True
    
    def deactivate(self):
        self.active = False
        self.background_sprite.visible = False
        
    
    # def tick(self):
    #     if self.active:
    #         self.background_sprite.visible = True
    #     else:
    #         self.background_sprite.visible = False