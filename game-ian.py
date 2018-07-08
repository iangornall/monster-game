import pygame, random, time

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

class Enemy(Character):
    def __init__(self, image_path, width, height, border_size, hero_x, hero_y, hero_width, hero_height):
        super(Enemy, self).__init__(image_path)
        # Place enemy at random position away from hero:
        left_side = range(border_size, int(hero_x))
        right_side = range(int(hero_x) + hero_width, width - border_size)
        x_possible = list(left_side) + list(right_side)
        self.x = random.choice(x_possible)
        top_side = range(border_size, int(hero_y))
        bottom_side = range(int(hero_y) + hero_height, height - border_size)
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
    def __init__(self, image_path, width, height, border_size, hero_x, hero_y, hero_width, hero_height):
        super(Monster, self).__init__(image_path, width, height, border_size, hero_x, hero_y, hero_width, hero_height)
        self.pace = 1

class Goblin(Enemy):
    def __init__(self, image_path, width, height, border_size, hero_x, hero_y, hero_width, hero_height):
        super(Goblin, self).__init__(image_path, width, height, border_size, hero_x, hero_y, hero_width, hero_height)
        self.pace = 0.5

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

def check_collision(hero, monster):
    if hero.x + hero.width < monster.x:
        return False
    if monster.x + monster.width < hero.x:
        return False
    if hero.y + hero.height < monster.y:
        return False
    if monster.y + monster.height < hero.y:
        return False
    return True

def main():
    width = 512
    height = 480
    level = 1
    win = False
    lose = False
    border_size = 32

    # Sounds and music
    pygame.mixer.init()
    win_sound = pygame.mixer.Sound('./sounds/win.wav')
    lose_sound = pygame.mixer.Sound('./sounds/lose.wav')
    music = pygame.mixer.music.load('./sounds/music.wav')
    pygame.mixer.music.play(loops=-1)
    

    # Game initialization
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()

    background = pygame.image.load('./images/background.png').convert_alpha()

    # Load characters
    hero = Hero('./images/hero.png', width, height)
    monster = Monster('./images/monster.png', width, height, border_size, hero.x, hero.y, hero.width, hero.height)
    goblins = []
    for i in range(level):
        goblins.append(Goblin('./images/goblin.png', width, height, border_size, hero.x, hero.y, hero.width, hero.height))

    # Bound coordinates over which characters can travel
    min_x = border_size
    max_x = width - border_size * 2
    min_y = border_size
    max_y = height - border_size * 2

    # Load messages
    font = pygame.font.Font(None, 25)
    level_text = font.render('Level: ' + str(level), True, (0, 0, 0))
    win_text = font.render('You win! Hit ENTER to play again!', True, (0, 0, 0))
    lose_text = font.render('You lose! Hit ENTER to play again!', True, (0, 0, 0))

    stop_game = False
    start_time = time.time() - 2.1
    while not stop_game:
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.KEYDOWN:
                # Handle game restart
                if (win or lose) and event.key == pygame.K_RETURN:
                    # Reset characters
                    hero = Hero('./images/hero.png', width, height)
                    monster = Monster('./images/monster.png', width, height, border_size, hero.x, hero.y, hero.width, hero.height)
                    goblins = []
                    for i in range(level):
                        goblins.append(Goblin('./images/goblin.png', width, height, border_size, hero.x, hero.y, hero.width, hero.height))

                    win = False
                    lose = False
                    pygame.mixer.music.play(loops=-1)
                    level_text = font.render('Level: ' + str(level), True, (0, 0, 0))
                # Handle hero control: moving
                try:
                    hero.start_moving[event.key]()
                except KeyError:
                    pass
            if event.type == pygame.KEYUP:
                # Handle hero control: stopping
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
            # Change direction of monster and goblins every two seconds
            if (time.time() - 2 > start_time):
                start_time += 2
                monster_direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
                monster.change_direction[monster_direction]()
                for goblin in goblins:
                    goblin_direction = random.choice(('north', 'east', 'south', 'west', 'northwest', 'northeast', 'southwest', 'southeast'))
                    goblin.change_direction[goblin_direction]()

            wrap = True
            monster.move(wrap, min_x, min_y, max_x, max_y)
            for goblin in goblins:
                goblin.move(wrap, min_x, min_y, max_x, max_y)
        # Winning
        if check_collision(hero, monster):
            monster.hide()
            for goblin in goblins:
                goblin.hide()
            pygame.mixer.music.stop()
            win_sound.play()
            win = True
            level += 1
        # Losing
        for goblin in goblins:
            if check_collision(hero, goblin):
                monster.hide()
                for goblin in goblins:
                    goblin.hide()
                pygame.mixer.music.stop()
                lose_sound.play()
                lose = True

        # Blit
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        screen.blit(level_text, (32, 32))
        hero.blit(screen)
        if not monster.hidden:
            monster.blit(screen)
            for goblin in goblins:
                goblin.blit(screen)
        if win:
            screen.blit(win_text, (width / 2 - win_text.get_width() / 2, height / 2 - win_text.get_height() / 2))
        elif lose:
            screen.blit(lose_text, (width / 2 - lose_text.get_width() / 2, height / 2 - lose_text.get_height() / 2))

        # Game display
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
