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
        self.start_x = self.x
        self.start_y = self.y
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
        self.hidden = False
    def hide(self):
        self.x = 0
        self.y = 0
        self.x_speed = 0
        self.y_speed = 0
        self.hidden = True
    

class Hero(Character):
    def __init__(self, image_path, screen_width, screen_height):
        super(Hero, self).__init__(image_path)
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.position_center(screen_width, screen_height)
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
    def position_center(self, screen_width, screen_height):
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height / 2 - self.height / 2
    def stopX(self):
        self.x_speed = 0
    def stopY(self):
        self.y_speed = 0

def check_collision(hero, monster):
    if hero.x + 32 < monster.x:
        return False
    if monster.x + 32 < hero.x:
        return False
    if hero.y + 32 < monster.y:
        return False
    if monster.y + 32 < hero.y:
        return False
    return True

def main():
    width = 512
    height = 480
    pygame.mixer.init()
    win_sound = pygame.mixer.Sound('./sounds/win.wav')
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()

    # Game initialization
    background = pygame.image.load('./images/background.png').convert_alpha()
    hero = Hero('./images/hero.png', width, height)

    monster = Monster('./images/monster.png', width, height, hero.x, hero.y, hero.width, hero.height)

    font = pygame.font.Font(None, 25)
    win_text = font.render('Hit ENTER to play again!', True, (0, 0, 0))
    show_win_text = False
 
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
                if monster.hidden and event.key == pygame.K_RETURN:
                    hero = Hero('./images/hero.png', width, height)
                    monster = Monster('./images/monster.png', width, height, hero.x, hero.y, hero.width, hero.height)
                    show_win_text = False
                try:
                    hero.start_moving[event.key]()
                except KeyError:
                    pass
            if event.type == pygame.KEYUP:
                try:
                    hero.stop_moving[event.key]()
                except KeyError:
                    pass
            if event.type == pygame.QUIT:
                stop_game = True
        
        # Game logic
        wrap = False
        hero.move(wrap, min_x, min_y, max_x, max_y)
        if not monster.hidden:
            if (time.time() - 2 > start):
                start += 2
                direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
                monster.change_direction[direction]()
            wrap = True
            monster.move(wrap, min_x, min_y, max_x, max_y)
        if check_collision(hero, monster):
            monster.hide()
            win_sound.play()
            show_win_text = True

        # Draw background
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        hero.blit(screen)
        if not monster.hidden:
            monster.blit(screen)
        if show_win_text:
            screen.blit(win_text, (width / 2 - win_text.get_width() / 2, height / 2 - win_text.get_height() / 2))


        # Game display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
