import pygame, random, time

class Monster(object):
    def __init__(self, image_path, width, height, hero_x, hero_y, hero_width, hero_height):
        self.image = pygame.image.load('./images/monster.png').convert_alpha()
        x_offset = random.randint(hero_width, width / 2 - hero_width * 1.5) * random.randrange(-1, 2, 2)
        self.x = hero_x - x_offset
        y_offset = random.randint(hero_height, height / 2 - hero_height * 1.5) * random.randrange(-1, 2, 2)
        self.y = hero_y - y_offset
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
    def move(self, min_x, min_y,
                    max_x, max_y):
        self.x += self.x_speed
        self.y += self.y_speed

        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x
    def north(self):
        self.y_speed = -1
    def east(self):
        self.x_speed = 1
    def south(self):
        self.y_speed = 1
    def west(self):
        self.x_speed = -1
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

def main():
    width = 512
    height = 480

    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()

    # Game initialization
    background = pygame.image.load('./images/background.png').convert_alpha()

    hero_image = pygame.image.load('./images/hero.png').convert_alpha()
    hero_width = hero_image.get_rect().width
    hero_x = width / 2 - hero_width / 2
    hero_height = hero_image.get_rect().height
    hero_y = height / 2 - hero_height / 2
    hero_x_speed = 0
    hero_y_speed = 0

    monster = Monster('./images/monster.png', width, height, hero_x, hero_y, hero_width, hero_height)

    min_x = hero_width
    max_x = width - hero_width * 2
    min_y = hero_height
    max_y = height - hero_height * 2

    stop_game = False
    start = time.time() - 2.1
    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    hero_y_speed = 0.9
                elif event.key == pygame.K_UP:
                    hero_y_speed = -0.9
                elif event.key == pygame.K_LEFT:
                    hero_x_speed = -0.9
                elif event.key == pygame.K_RIGHT:
                    hero_x_speed = 0.9
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    hero_y_speed = 0
                elif event.key == pygame.K_UP:
                    hero_y_speed = 0
                elif event.key == pygame.K_LEFT:
                    hero_x_speed = 0
                elif event.key == pygame.K_RIGHT:
                    hero_x_speed = 0
            if event.type == pygame.QUIT:
                stop_game = True
        
        # Game logic
        # if time.time() % 2 == 0:
        #     direction = random.choice(('north', 'east', 'south', 'west'))
        hero_y += hero_y_speed
        hero_x += hero_x_speed
        if hero_y < min_y:
            hero_y = min_y
        elif hero_y > max_y:
            hero_y = max_y
        if hero_x < min_x:
            hero_x = min_x
        elif hero_x > max_x:
            hero_x = max_x
        if (time.time() - 2 > start):
            start += 2
            direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
            monster.change_direction[direction]()
        monster.move(min_x, min_y, max_x, max_y)

        # Draw background
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        screen.blit(hero_image, (hero_x, hero_y))
        monster.blit(screen)

        # Game display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
