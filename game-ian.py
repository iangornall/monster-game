import pygame, random, time

class Monster(object):
    def __init__(self, image_path, width, height, hero_x, hero_y, hero_width, hero_height):
        self.image = pygame.image.load('./images/monster.png').convert_alpha()
        x_offset = random.randint(hero_width, width / 2 - hero_width * 1.5) * random.randrange(-1, 2, 2)
        self.x = hero_x - x_offset
        y_offset = random.randint(hero_height, height / 2 - hero_height * 1.5) * random.randrange(-1, 2, 2)
        self.y = hero_y - y_offset
        self.move = {'north': self.move_north, 
                    'east': self.move_east, 
                    'south': self.move_south, 
                    'west': self.move_west, 
                    'northwest': self.move_northwest, 
                    'northeast': self.move_northeast, 
                    'southwest': self.move_southwest, 
                    'southeast': self.move_southeast}
    def move_north(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.y -= 1
        if self.y < min_y:
            self.y = max_y
    def move_east(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.x += 1
        if self.x > max_x:
            self.x = min_x
    def move_south(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.y += 1
        if self.y > max_y:
            self.y = min_y
    def move_west(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.x -= 1
        if self.x < min_x:
            self.x = max_x
    def move_northwest(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.move_north(clock, min_x, min_y, max_x, max_y)
        self.move_west(clock, min_x, min_y, max_x, max_y)
        clock.tick(60)
    def move_northeast(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.move_north(clock, min_x, min_y, max_x, max_y)
        self.move_east(clock, min_x, min_y, max_x, max_y)
        clock.tick(60)
    def move_southwest(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.move_south(clock, min_x, min_y, max_x, max_y)
        self.move_west(clock, min_x, min_y, max_x, max_y)
        clock.tick(60)
    def move_southeast(self, clock,
                    min_x, min_y,
                    max_x, max_y):
        self.move_south(clock, min_x, min_y, max_x, max_y)
        self.move_east(clock, min_x, min_y, max_x, max_y)
        clock.tick(60)
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
            if event.type == pygame.QUIT:
                stop_game = True
        
        # Game logic
        # if time.time() % 2 == 0:
        #     direction = random.choice(('north', 'east', 'south', 'west'))
        if (time.time() - 2 > start):
            start += 2
            direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
        monster.move[direction](clock, min_x, min_y, max_x, max_y)

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
