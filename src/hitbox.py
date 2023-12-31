from src.helpers.interfaces import Pair


class Hitbox:
    def __init__(self, pos: Pair, width: int, height: int) -> None:
        self.pos = pos
        self.width = width
        self.height = height

    def copy(self):
        new_copy = Hitbox(pos=self.pos.copy(), width=self.width, height=self.height)

        return new_copy

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