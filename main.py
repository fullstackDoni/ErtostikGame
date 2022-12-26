import pygame, sys
from fighter import Fighter

from menu.button import Button

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ertostik Oqigalary")
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ertostik Oqigalary")

BG = pygame.image.load("menu/assets/Background.png")
pygame.mixer.music.load("assets/audio/music.mp3")


def get_font(size):
    return pygame.font.Font("menu/assets/font.ttf", size)


def play():
    clock = pygame.time.Clock()
    FPS = 60

    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLUE = (11, 81, 130)
    GREEN = (140, 231, 49)

    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000

    ERTOSTIK_SIZE = 162
    ERTOSTIK_SCALE = 4
    ERTOSTIK_OFFSET = [72, 56]
    ERTOSTIK_DATA = [ERTOSTIK_SIZE, ERTOSTIK_SCALE, ERTOSTIK_OFFSET]
    MYSTAN_SIZE = 250
    MYSTAN_SCALE = 3
    MYSTAN_OFFSET = [112, 107]
    MYSTAN_DATA = [MYSTAN_SIZE, MYSTAN_SCALE, MYSTAN_OFFSET]


    pygame.mixer.music.load("assets/audio/music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
    sword_fx.set_volume(0.5)
    magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
    magic_fx.set_volume(0.75)

    bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

    ertostik_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    mystan_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()


    victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()


    ERTOSTIK_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    MYSTAN_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_bg():
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))


    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

    fighter1 = Fighter(1, 200, 310, False, ERTOSTIK_DATA, ertostik_sheet, ERTOSTIK_ANIMATION_STEPS, sword_fx)
    fighter2 = Fighter(2, 800, 310, True, MYSTAN_DATA, mystan_sheet, MYSTAN_ANIMATION_STEPS, magic_fx)

    run = True
    while run:

        clock.tick(FPS)

        draw_bg()

        draw_health_bar(fighter1.health, 20, 20)
        draw_health_bar(fighter2.health, 860, 20)
        draw_text("Ertostik: " + str(score[0]), score_font, BLUE, 20, 60)
        draw_text("Mystan: " + str(score[1]), score_font, BLUE, 860, 60)


        if intro_count <= 0:

            fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter2, round_over)
            fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter1, round_over)
        else:

            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)

            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()


        fighter1.update()
        fighter2.update()


        fighter1.draw(screen)
        fighter2.draw(screen)


        if round_over == False:
            if fighter1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (500, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter1 = Fighter(1, 200, 410, False, ERTOSTIK_DATA, ertostik_sheet, ERTOSTIK_ANIMATION_STEPS, sword_fx)
                fighter2 = Fighter(2, 700, 310, True, MYSTAN_DATA, mystan_sheet,MYSTAN_ANIMATION_STEPS , magic_fx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Jasagan: Nurlybek & Daniyar", True, "Black")

        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))

        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="Artqa", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Ertostik Oqigasy", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(650, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("menu/assets/Play Rect.png"), pos=(640, 250),
                             text_input="Bastau", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("menu/assets/Options Rect.png"), pos=(640, 400),
                                text_input="Biz jaily", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("menu/assets/Quit Rect.png"), pos=(640, 550),
                             text_input="Shygu", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
