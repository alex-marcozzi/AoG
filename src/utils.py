import pyglet

def add_tuples(t1: tuple, t2: tuple):
    return tuple(map(lambda x, y: x + y, t1, t2))