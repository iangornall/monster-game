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
    heroWidth = hero_image.get_rect().width
    heroX = width / 2 - heroWidth / 2
    heroHeight = hero_image.get_rect().height
    heroY = height / 2 - heroHeight / 2
    monster_image = pygame.image.load('./images/monster.png').convert_alpha()
    monsterXOffset = random.randint(heroWidth, width / 2 - heroWidth * 1.5) * random.randrange(-1, 2, 2)
    monsterYOffset = random.randint(heroHeight, height / 2 - heroHeight * 1.5) * random.randrange(-1, 2, 2)
    stop_game = False
    while not stop_game:
        for event in pygame.event.get():

            # Event handling

            if event.type == pygame.QUIT:
                stop_game = True


        # Game logic

        # Draw background
        screen.blit(background, (0, 0))
        
        screen.blit(hero_image, (heroX, heroY))
        screen.blit(monster_image, 
                    (heroX - monsterXOffset,
                    heroY - monsterYOffset))


        # Game display

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
