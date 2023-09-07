import os
import pyglet
from src.engine import Engine
from src.entity import Entity

window = pyglet.window.Window()

camera_x = 0
camera_y = 0

engine = Engine(window)
entity = Entity(window, "assets/images/orange.png", global_pos=(0, 0), velocity=(0.1,0), acceleration=(0,0))

@window.event
def on_key_press(symbol, modifiers):
    global camera_x
    global camera_y
    
    if symbol == pyglet.window.key.W:
        camera_y = camera_y + 5
    if symbol == pyglet.window.key.A:
        camera_x = camera_x - 5
    if symbol == pyglet.window.key.S:
        camera_y = camera_y - 5
    if symbol == pyglet.window.key.D:
        camera_x = camera_x + 5
    engine.handle_key_press(symbol, modifiers)

@window.event
def on_key_release(symbol, modifiers):
    engine.handle_key_release(symbol, modifiers)

@window.event
def on_draw():
    entity.tick()
    window.clear()
    entity.draw((camera_x,camera_y))
    # engine.draw()

pyglet.app.run()