import os
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Menu:
    def __init__(self):
        self.in_menu = True
        self.run_menu()

    def draw_menu(self):
        pygame.mouse.set_visible(True)
        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        screen.fill(pygame.Color('black'))
        screen.blit(load_image('images\\menu_background.jpg'), (0, 0))
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 3, width // 2, height // 6), 5)
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 4, height // 3 * 2, width // 2, height // 6), 5)
        font = pygame.font.Font(None, 290)
        screen.blit(font.render("Space Shoot", 1, pygame.Color('red')),
                    (100, 100))
        font = pygame.font.Font(None, 200)
        screen.blit(font.render("Играть", 1, pygame.Color('red')),
                    (width // 3 + 70, height // 3 + 20))
        screen.blit(font.render("Выход", 1, pygame.Color('red')),
                    (width // 3 + 70, height // 3 * 2 + 20))


pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60
