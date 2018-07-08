import pygame
from character import Character

class Hero(Character):
    def __init__(self, image_path, screen_width, screen_height):
        super(Hero, self).__init__(image_path)
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height / 2 - self.height / 2
        self.pace = 0.9
        self.x_speed = 0
        self.y_speed = 0
        self.start_moving = {pygame.K_DOWN: self.south, 
                                pygame.K_UP: self.north, 
                                pygame.K_LEFT: self.west,
                                pygame.K_RIGHT: self.east}
        self.stop_moving = {pygame.K_DOWN: self.stopY,
                                pygame.K_UP: self.stopY,
                                pygame.K_LEFT: self.stopX,
                                pygame.K_RIGHT: self.stopX}
    def stopX(self):
        self.x_speed = 0
    def stopY(self):
        self.y_speed = 0