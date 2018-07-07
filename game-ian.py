import pygame, random

def move_north(x, y,
                min_x, min_y,
                max_x, max_y):
    new_y = y - 1
    if new_y < min_y:
        new_y = max_y
    return (x, new_y)

def move_east(x, y,
                min_x, min_y,
                max_x, max_y):
    new_x = x + 1
    if new_x > max_x:
        new_x = min_x
    return (new_x, y)

def move_south(x, y,
                min_x, min_y,
                max_x, max_y):
    new_y = y + 1
    if new_y > max_y:
        new_y = min_y
    return (x, new_y)

def move_west(x, y,
                min_x, min_y,
                max_x, max_y):
    new_x = x - 1
    if new_x < min_x:
        new_x = max_x
    return (new_x, y)

def main():
    width = 512
    height = 480
    move = {'north': move_north, 'east': move_east, 'south': move_south, 'west': move_west}

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

    monster_image = pygame.image.load('./images/monster.png').convert_alpha()
    monster_x_offset = random.randint(hero_width, width / 2 - hero_width * 1.5) * random.randrange(-1, 2, 2)
    monster_x = hero_x - monster_x_offset
    monster_y_offset = random.randint(hero_height, height / 2 - hero_height * 1.5) * random.randrange(-1, 2, 2)
    monster_y = hero_y - monster_y_offset
    min_x = hero_width
    max_x = width - hero_width * 2
    min_y = hero_height
    max_y = height - hero_height * 2

    count = 1

    stop_game = False
    while not stop_game:
        for event in pygame.event.get():

            # Event handling

            if event.type == pygame.QUIT:
                stop_game = True
        if count == 1:
            direction = random.choice(('north', 'east', 'south', 'west'))
        elif count == 120:
            count = 0
        count += 1
        # Game logic
        monster_x, monster_y = move[direction](
            monster_x, monster_y, min_x, min_y, max_x, max_y)

        # Draw background
        screen.fill([255,255,255])
        screen.blit(background, (0, 0))
        screen.blit(hero_image, (hero_x, hero_y))
        screen.blit(monster_image, 
                    (monster_x,
                    monster_y))


        # Game display

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
