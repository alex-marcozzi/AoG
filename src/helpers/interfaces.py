import pyglet


class Pair:
    def __init__(self, first: any, second: any):
        self.first = first
        self.second = second

    def copy(self):
        return Pair(self.first, self.second)

    def add(self, other):
        if type(other) is Pair:
            self.first += other.first
            self.second += other.second

        return self
