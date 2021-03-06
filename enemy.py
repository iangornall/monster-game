import pygame, random
from character import Character

class Enemy(Character):
    def __init__(self, image_path, width, height, border_size, hero):
        super(Enemy, self).__init__(image_path)
        # Place enemy at random position away from hero:
        left_side = range(border_size, int(hero.x))
        right_side = range(int(hero.x) + hero.width, width - border_size)
        x_possible = list(left_side) + list(right_side)
        self.x = random.choice(x_possible)
        top_side = range(border_size, int(hero.y))
        bottom_side = range(int(hero.y) + hero.height, height - border_size)
        y_possible = list(top_side) + list(bottom_side)
        self.y = random.choice(y_possible)
        
        self.pace = None
        self.x_speed = 0
        self.y_speed = 0
        self.change_direction = {'north': self.north, 
                    'east': self.east, 
                    'south': self.south, 
                    'west': self.west, 
                    'northwest': self.northwest, 
                    'northeast': self.northeast, 
                    'southwest': self.southwest, 
                    'southeast': self.southeast}
        self.hidden = False
    def hide(self):
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.hidden = True

class Monster(Enemy):
    def __init__(self, image_path, width, height, border_size, hero):
        super(Monster, self).__init__(image_path, width, height, border_size, hero)
        self.pace = 1

class Goblin(Enemy):
    def __init__(self, image_path, width, height, border_size, hero):
        super(Goblin, self).__init__(image_path, width, height, border_size, hero)
        self.pace = 0.5