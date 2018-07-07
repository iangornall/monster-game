import pygame, random, time

class Character(object):
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
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


class Monster(Character):
    def __init__(self, image_path, width, height, hero_x, hero_y, hero_width, hero_height):
        super(Monster, self).__init__(image_path)
        x_offset = random.randint(hero_width, width / 2 - hero_width * 1.5) * random.randrange(-1, 2, 2)
        self.x = hero_x - x_offset
        y_offset = random.randint(hero_height, height / 2 - hero_height * 1.5) * random.randrange(-1, 2, 2)
        self.y = hero_y - y_offset
        self.pace = 1
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
    

class Hero(Character):
    def __init__(self, image_path, width, height):
        super(Hero, self).__init__(image_path)
        self.width = self.image.get_rect().width
        self.x = width / 2 - self.width / 2
        self.height = self.image.get_rect().height
        self.y = height / 2 - self.height / 2
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

def main():
    width = 512
    height = 480

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()

    # Game initialization
    background = pygame.image.load('./images/background.png').convert_alpha()
    hero = Hero('./images/hero.png', width, height)

    monster = Monster('./images/monster.png', width, height, hero.x, hero.y, hero.width, hero.height)
 
    min_x = hero.width
    max_x = width - hero.width * 2
    min_y = hero.height
    max_y = height - hero.height * 2

    stop_game = False
    start = time.time() - 2.1
    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.KEYDOWN:
                try:
                    hero.start_moving[event.key]()
                except:
                    print('Invalid key')
            if event.type == pygame.KEYUP:
                try:
                    hero.stop_moving[event.key]()
                except:
                    print('Invalid key')
            if event.type == pygame.QUIT:
                stop_game = True
        
        # Game logic
        # if time.time() % 2 == 0:
        #     direction = random.choice(('north', 'east', 'south', 'west'))
        wrap = False
        hero.move(wrap, min_x, min_y, max_x, max_y)
        if (time.time() - 2 > start):
            start += 2
            direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
            monster.change_direction[direction]()
        wrap = True
        monster.move(wrap, min_x, min_y, max_x, max_y)

        # Draw background
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        hero.blit(screen)
        monster.blit(screen)

        # Game display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
