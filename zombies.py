import arcade as a
from constants import *
import animate


class Zombie(animate.Animate):
    def __init__(self, image, health, speed, row, center_y, window):
        super().__init__(image, 0.09)
        self.health = health
        self.change_x = speed
        self.row = row
        self.set_position(SCREEN_WIDTH, center_y)
        self.eating = False
        self.window = window
    def update(self):
        if not self.eating:
            self.center_x -= self.change_x
        if self.health <= 0:
            self.kill()
            self.window.killed_zombies += 1
            self.window.attack_time -= 1
        self.eating = False
        food = a.check_for_collision_with_list(self, self.window.plants_list)
        for i in food:
            if self.row == i.row:
                self.eating = True
                i.health -= 0.5
        if self.right < FIELD_LEFT:
            self.window.run = False



class Republican_Zombie(Zombie):
    def __init__(self, row, center_y, window):
        super().__init__("zombies/zom1.png", 12, 0.2, row, center_y, window)
        self.append_texture(a.load_texture("zombies/zom2.png"))
class Bucket_Zombie(Zombie):
    def __init__(self, row, center_y, window):
        super().__init__("zombies/buck1.png", 32, 0.2, row, center_y, window)
        self.append_texture(a.load_texture("zombies/buck2.png"))
class Cone_Head_Zombie(Zombie):
    def __init__(self, row, center_y, window):
        super().__init__("zombies/cone1.png", 20, 0.2, row, center_y, window)
        self.append_texture(a.load_texture("zombies/cone2.png"))