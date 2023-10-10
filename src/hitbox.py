from src.helpers.interfaces import Pair


class Hitbox:
    def __init__(self, pos: Pair, width: int, height: int) -> None:
        self.pos = pos
        self.width = width
        self.height = height

    def bottomLeft(self):
        return self.pos

    def bottomRight(self):
        return Pair(self.pos.first + self.width, self.pos.second)

    def topLeft(self):
        return Pair(self.pos.first, self.pos.second + self.height)

    def topRight(self):
        return Pair(
            self.pos.first + self.width,
            self.pos.second + self.height,
        )