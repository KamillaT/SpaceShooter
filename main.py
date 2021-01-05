import math
import os
from random import uniform

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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, walls_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x + 23, y + 6, 57, 75)
        self.left = x + 23
        self.top = y + 6
        self.right = self.left + 57
        self.bottom = self.top + 75


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        pygame.key.set_repeat(10, 1)
        self.image = load_image('images\\player.png', -1)
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y
        self.direction = 'right'
        self.room = [self.x // 1280, self.y // 1280]
        self.in_corridor = False
        self.walk_cycle = 0
        self.hp = 3
        self.hitbox = Hitbox(self.x, self.y)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.gold = 0
        self.gun = Pistol(self.rect.left, self.rect.top)

    def move(self, dir, n):
        self.rect[dir] += 5 * n
        self.hitbox.rect[dir] += 5 * n
        if dir == 0:
            self.x += 5 * n
            self.hitbox.left += 5 * n
            self.hitbox.right += 5 * n
        else:
            self.y += 5 * n
            self.hitbox.top += 5 * n
            self.hitbox.bottom += 5 * n

        self.room = [self.x // 1280, self.y // 1280]
        self.in_corridor = self.hitbox.left % 1280 > 895 or self.hitbox.top % 1280 > 895 \
                           or self.hitbox.right % 1280 < 64 or self.hitbox.bottom % 1280 < 64 or \
                           self.hitbox.left % 1280 < 64 or self.hitbox.top % 1280 < 64 or \
                           self.hitbox.right % 1280 > 895 or self.hitbox.bottom % 1280 > 895


class Gun(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(gun_group)
        self.normal_image = load_image('images\\pistol.png', -1)
        self.image = load_image('images\\pistol.png', -1)
        self.x = tile_width * pos_x + 75
        self.y = tile_height * pos_y + 40
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.damage = 5
        self.bv = 10

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.left, mouse_y - self.rect.top
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        if angle < -90 or angle > 90:
            self.image = pygame.transform.flip(self.normal_image, True, False)
            self.image = pygame.transform.rotate(self.image, int(angle) - 180)
        else:
            self.image = pygame.transform.rotate(self.normal_image, int(angle))
        self.rect = self.image.get_rect(center=(983, 560))


class Pistol(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\pistol.png', -1)
        self.image = load_image('images\\pistol.png', -1)
        self.bv = 10
        self.damage = 5
        self.gap = 20

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 30)


class Pistol1(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\pistol1.png', -1)
        self.image = load_image('images\\pistol1.png', -1)
        self.bv = 30
        self.damage = 15
        self.gap = 30

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 100)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, v, damage, uni):
        super().__init__(bullet_group, all_sprites)
        self.x = player.rect.left + 55
        self.y = player.rect.top + 40
        rx = x - self.x
        ry = y - self.y
        angle = (180 / math.pi) * math.atan2(rx, ry)
        angle = uniform(angle - 180 / uni, angle + 180 / uni)
        self.vx = math.sin(angle / 180 * math.pi) * v
        self.vy = math.cos(angle / 180 * math.pi) * v
        self.damage = damage
        self.image = load_image('images\\bullet.png', -1)
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.sx, self.sy = self.rect.center

        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image, int(angle))

    def update(self):
        self.sx = self.sx + self.vx
        self.sy = self.sy + self.vy
        self.rect.left = self.sx
        self.rect.top = self.sy


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

    def run_menu(self):
        global in_game
        self.draw_menu()
        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in range(width // 4, width // 4 * 3):
                        if event.pos[1] in range(height // 3, height // 2):
                            self.in_menu = False
                            in_game = True
                        elif event.pos[1] in range(height // 3 * 2, height // 6 * 5):
                            self.in_menu = False
            clock.tick(fps)
            pygame.display.flip()


pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
fps = 60

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
tile_images = {'wall': load_image('images\\wall.png'),
               'empty': load_image('images\\floor.png'),
               'hole': load_image('images\\hole.png')}
tile_width = 64
tile_height = 64
