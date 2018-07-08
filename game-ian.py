import pygame, random, time
from hero import Hero
from enemy import Monster, Goblin

def check_collision(hero, enemy):
    if hero.x + hero.width < enemy.x:
        return False
    if enemy.x + enemy.width < hero.x:
        return False
    if hero.y + hero.height < enemy.y:
        return False
    if enemy.y + enemy.height < hero.y:
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
