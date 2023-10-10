import pyglet
import time


class Attack:
    def __init__(
        self,
        hitboxes: list,
        duration: float,
        damage: int,
    ):
        self.hitboxes = hitboxes
        self.duration = duration
        self.damage = damage

        self.thrown_time = None

    def Throw(self):
        # if attack already in progress, we have to wait until it's finished to throw again
        if self.inProgress():
            return

        self.thrown_time = time.time()

    def inProgress(self):
        now = time.time()
        if self.thrown_time and now <= self.thrown_time + self.duration:
            return True
        
        return False

    # def Hit(self, character: Character):
    #     # when we add modifiers later we could do checking here:
    #     # if "poisonous" in self.modifiers:
    #     #       etc.

    #     character.takeDamage(amount=self.damage)