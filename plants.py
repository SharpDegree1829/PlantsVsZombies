import arcade as a
import animate
import time

import zombies
from constants import SCREEN_WIDTH

class Plant(animate.Animate):
    def __init__(self, image, health, cost, window):
        super().__init__(image, 0.12)
        self.health = health
        self.cost = cost
        self.row = 0
        self.column = 0
        self.window = window
    def update(self):
        if self.health <= 0:
            self.kill()
            self.window.lawns.remove((self.row, self.column))
    def planting(self, center_x, center_y, row, column):
        self.set_position(center_x, center_y)
        self.row = row
        self.column = column
class Sunflower(Plant):
    def __init__(self, window):
        super().__init__("plants/sun1.png", 60, 50, window)
        self.append_texture(a.load_texture("plants/sun1.png"))
        self.append_texture(a.load_texture("plants/sun2.png"))
        self.sun_spawn_time = time.time()
        self.sunspawn_sound = a.load_sound("sounds/sunspawn.mp3")
    def update(self):
        super().update()
        if time.time() - self.sun_spawn_time >= 15:
            new_sun = Sun(self.right, self.bottom)
            self.sun_spawn_time = time.time()
            self.window.sun_list.append(new_sun)
            self.sunspawn_sound.play()
class Sun(a.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__("items/sun.png", 0.12)
        self.center_x = center_x
        self.center_y = center_y
        self.sun_time = time.time()
    def update(self):
        self.angle += 1
        if time.time() - self.sun_time >= 5:
            self.kill()
class Pea_Shooter(Plant):
    def __init__(self, window):
        super().__init__("plants/pea1.png", 100, 100, window)
        self.append_texture(a.load_texture("plants/pea2.png"))
        self.append_texture(a.load_texture("plants/pea3.png"))
        self.pea_spawn_time = time.time()
    def update(self):
        super().update()
        zombie_on_row = False
        for zombie in self.window.zombie_list:
            if zombie.row == self.row:
                zombie_on_row = True
        if time.time() - self.pea_spawn_time >= 2 and zombie_on_row:
            new_pea = Pea(self.right, self.top, self.window)
            self.pea_spawn_time = time.time()
            self.window.pea_list.append(new_pea)

class Pea(a.Sprite):
    def __init__(self, center_x, center_y, window):
        super().__init__("items/bul.png", 0.12)
        self.center_x = center_x
        self.center_y = center_y
        self.change_x = 7
        self.damage = 1
        self.window = window
        self.hit_sound = a.load_sound("sounds/hit.mp3")
    def update(self):
        self.center_x += self.change_x
        if self.center_x > SCREEN_WIDTH:
            self.kill()
        hit_list = a.check_for_collision_with_list(self, self.window.zombie_list)
        if hit_list:
            for zombie in hit_list:
                zombie.health -= self.damage
            self.kill()
            self.hit_sound.play()

class Nut(Plant):
    def __init__(self, window):
        super().__init__("plants/nut1.png", 300, 50, window)
        self.append_texture(a.load_texture("plants/nut2.png"))
        self.append_texture(a.load_texture("plants/nut3.png"))
class Tree(Plant):
    def __init__(self, window):
        super().__init__("plants/tree1.png", 150, 175, window)
        self.append_texture(a.load_texture("plants/tree2.png"))
        self.append_texture(a.load_texture("plants/tree3.png"))
    def update(self):
        super().update()
        hit_list = a.check_for_collision_with_list(self, self.window.pea_list)
        for pea in hit_list:
            pea.texture = a.load_texture("items/firebul.png")
            pea.damage = 3
