import pygame
import sys
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum

pygame.init()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, text_color, bg_color, action=None):
        super().__init__()

        self.mouse_over = False

        default_image = menu_surface_with_text(text, font_size, text_color, bg_color)
        highlighted_image = menu_surface_with_text(text, font_size * 1.2, text_color, bg_color)

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)]
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEW_GAME = 1
    SETTINGS = 2
    SKIN = 3
    SHIMITO = 4
    HEITOR = 5


def menu_surface_with_text(text, font_size, text_color, bg_color):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_color, bgcolor=bg_color)
    return surface.convert_alpha()


def title_screen(screen):
    start_button = UIElement(
        center_position=(144, 150),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Start',
        action=GameState.NEW_GAME
    )
    settings_button = UIElement(
        center_position=(144, 250),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Settings',
        action=GameState.SETTINGS
    )
    quit_button = UIElement(
        center_position=(144, 350),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Quit',
        action=GameState.QUIT
    )
    buttons = [start_button, settings_button, quit_button]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(black)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                return ui_action

            button.draw(screen)

        pygame.display.flip()


def settings_menu(screen):
    skin_button = UIElement(
        center_position=(144, 200),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Skin',
        action=GameState.SKIN
    )

    back_button = UIElement(
        center_position=(144, 300),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Back',
        action=GameState.TITLE
    )
    
    buttons = [skin_button, back_button]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(black)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                return ui_action

            button.draw(screen)

        pygame.display.flip()


def choose_skin(screen):
    skin1 = UIElement(
        center_position=(144, 200),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Shimito',
        action=GameState.SHIMITO
    )

    skin2 = UIElement(
        center_position=(144, 300),
        font_size=30,
        bg_color=black,
        text_color=white,
        text='Heitor',
        action=GameState.HEITOR
    )

    skins = [skin1, skin2]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(black)

        for skin in skins:
            ui_action = skin.update(pygame.mouse.get_pos(), mouse_up)

            if ui_action is not None:
                return ui_action

            skin.draw(screen)

        pygame.display.flip()


def choice_character(character):
    if character == 'shimito':
        
        bird_upflap = pygame.image.load('assets/dinho2.png')
        bird_midflap = pygame.image.load('assets/dinho2.png')
        bird_downflap = pygame.image.load('assets/dinho2.png')

    elif character == 'heitor':
        
        bird_upflap = pygame.image.load('assets/heitor.png')
        bird_midflap = pygame.image.load('assets/heitor.png')
        bird_downflap = pygame.image.load('assets/heitor.png')

    else:
        
        bird_upflap = pygame.image.load('assets/yellowbird-upflap.png')
        bird_midflap = pygame.image.load('assets/yellowbird-midflap.png')
        bird_downflap = pygame.image.load('assets/yellowbird-downflap.png')

    return [bird_upflap, bird_midflap, bird_downflap]


def main(scr, character):
    game_state = GameState.TITLE

    screen = scr

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        elif game_state == GameState.NEW_GAME:
                return choice_character(character)

        elif game_state == GameState.SETTINGS:
                game_state = settings_menu(screen)

                if game_state == GameState.SKIN:
                    game_state = choose_skin(screen)

                    if game_state == GameState.SHIMITO:
                        character = 'shimito'

                    elif game_state == GameState.HEITOR:
                        character = 'heitor'

                game_state = title_screen(screen)

        elif game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()
    

black = (0, 0, 0)
white = (255, 255, 255)