import pygame, random

def main():
    width = 512
    height = 480
    blue_color = (97, 159, 182)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
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
    min_x_position = hero_width
    max_x_position = width - hero_width * 2
    min_y_position = hero_height
    max_y_position = height - hero_height * 2

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
        # Game logic
        if direction == 'north':
            monster_y -= 1
            if monster_y < min_y_position:
                monster_y = max_y_position
        elif direction == 'east':
            monster_x += 1
            if monster_x > max_x_position:
                monster_x = min_x_position
        elif direction == 'south':
            monster_y += 1
            if monster_y > max_y_position:
                monster_y = min_y_position
        elif direction == 'west':
            monster_x -= 1
            if monster_x < min_x_position:
                monster_x = max_x_position


        

        # Draw background
        screen.blit(background, (0, 0))
        
        screen.blit(hero_image, (hero_x, hero_y))
        screen.blit(monster_image, 
                    (monster_x,
                    monster_y))


        # Game display

        pygame.display.update()
        clock.tick(60)
        count += 1

    pygame.quit()

if __name__ == '__main__':
    main()
