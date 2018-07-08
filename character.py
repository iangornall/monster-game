import pygame
class Character(object):
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.x = None
        self.y = None
        self.pace = None
        self.x_speed = None
        self.y_speed = None
        
    def move(self, wrap, min_x, min_y,
                    max_x, max_y):
        self.x += self.x_speed
        self.y += self.y_speed
        if wrap:
            if self.y < min_y:
                self.y = max_y
            elif self.y > max_y:
                self.y = min_y
            if self.x < min_x:
                self.x = max_x
            elif self.x > max_x:
                self.x = min_x
        else:
            if self.y < min_y:
                self.y = min_y
            elif self.y > max_y:
                self.y = max_y
            if self.x < min_x:
                self.x = min_x
            elif self.x > max_x:
                self.x = max_x
    def north(self):
        self.y_speed = -1 * self.pace
    def east(self):
        self.x_speed = self.pace
    def south(self):
        self.y_speed = self.pace
    def west(self):
        self.x_speed = -1 * self.pace
    def northwest(self):
        self.north()
        self.west()
    def northeast(self):
        self.north()
        self.east()
    def southwest(self):
        self.south()
        self.west()
    def southeast(self):
        self.south()
        self.east()
    def blit(self, screen):
        screen.blit(self.image, (self.x, self.y))