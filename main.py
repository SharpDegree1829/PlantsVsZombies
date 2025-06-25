import time

import arcade as a
import random
import plants
from constants import *
import zombies

def lawn_x(x):
    right_x = 247 + CELL_WIDTH
    column = 1
    while right_x < x:
        right_x += CELL_WIDTH
        column += 1
    center_x = right_x - CELL_WIDTH / 2
    return center_x, column
def lawn_y(y):
    top_y = 28 + CELL_HEIGHT
    row = 1
    while top_y <= y:
        top_y += CELL_HEIGHT
        row += 1
    center_y = top_y - CELL_HEIGHT / 2
    return  center_y, row

class Game(a.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = a.load_texture("textures/background.jpg")
        self.menu = a.load_texture("textures/menu_vertical.png")
        self.plants_list = a.SpriteList()
        self.seed = None
        self.lawns = []
        self.seed_sound = a.load_sound("sounds/seed.mp3")
        self.suns = 300
        self.sun_list = a.SpriteList()
        self.pea_list = a.SpriteList()
        self.zombie_list = a.SpriteList()
        self.zombie_spawn_time = time.time()
        self.run = True
        self.endgame = a.load_texture("textures/end.png")
        self.killed_zombies = 0
        self.attack_time = 25
    def setup(self):
        pass
    def on_draw(self):
        a.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        a.draw_texture_rectangle(67, SCREEN_HEIGHT/2, 134, SCREEN_HEIGHT, self.menu)
        a.draw_text(self.suns, 65, SCREEN_HEIGHT - 105, a.color.BLACK, 27, anchor_x="center")
        self.plants_list.draw()
        self.sun_list.draw()
        self.pea_list.draw()
        self.zombie_list.draw()
        if self.seed != None:
            self.seed.draw()
        if not self.run:
            a.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.endgame)
    def update(self, delta_time: float):
        if self.run:
            self.plants_list.update()
            self.plants_list.update_animation(delta_time)
            self.sun_list.update()
            self.pea_list.update()
            self.zombie_list.update()
            self.zombie_list.update_animation(delta_time)
            if time.time() - self.zombie_spawn_time >= self.attack_time and self.killed_zombies <= 20:
                center_y, row = lawn_y(random.randint(28, 521))
                zombie_type = random.randint(1, 3)
                if zombie_type == 1:
                    self.zombie_list.append(zombies.Republican_Zombie(row, center_y, self))
                elif zombie_type == 2:
                    self.zombie_list.append(zombies.Cone_Head_Zombie(row, center_y, self))
                else:
                    self.zombie_list.append(zombies.Bucket_Zombie(row, center_y, self))
                self.zombie_spawn_time = time.time()
            if self.killed_zombies >= 20 and len(self.zombie_list) == 0:
                self.run = False
                self.endgame = a.load_texture("textures/logo.png")
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.run:
            if 16 <= x <= 113:
                if 375 <= y <= 482:
                    print("Sunflower")
                    self.seed = plants.Sunflower(self)
                if 261 <= y <= 367:
                    print("Green bean")
                    self.seed = plants.Pea_Shooter(self)
                if 146 <= y <= 252:
                    print("Wallnut")
                    self.seed = plants.Nut(self)
                if 31 <= y <= 136:
                    print("Torchwood")
                    self.seed = plants.Tree(self)
                if self.seed != None:
                    self.seed.center_x = x
                    self.seed.center_y = y
                    self.seed.alpha = 150
            for sun in self.sun_list:
                if sun.left <= x <= sun.right and sun.bottom <= y <= sun.top:
                    sun.kill()
                    self.suns += 25

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.run:
            if self.seed != None:
                self.seed.center_x = x
                self.seed.center_y = y

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if 247 <= x <= 960 and 28 <= y <= 521 and self.seed != None:
            center_x, column = lawn_x(x)
            center_y, row = lawn_y(y)
            if (row, column) in self.lawns or self.suns < self.seed.cost:
                self.seed = None
                return
            self.lawns.append((row, column))
            self.seed.planting(center_x, center_y, row, column)
            self.seed.alpha = 255
            self.plants_list.append(self.seed)
            a.play_sound(self.seed_sound, 0.7)
            self.suns -= self.seed.cost
            self.seed = None
        else:
            self.seed = None



window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
a.run()