import math
import os
from random import uniform, randint, shuffle
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


def load_music(name):
    fullname = os.path.join('data\\music', name)
    sound = pygame.mixer.Sound(fullname)
    sound.play()


def background_music():
    fullname = os.path.join('data\\music', 'background_music_.mp3')
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play(-1)


def load_menu_music():
    fullname = os.path.join('data\\music','background_music_2.mp3')
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.play(-1)


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


class TempWall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, bullet_stopper_group)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.cond = 0

    def update(self):
        self.cond += 1
        if self.cond == 1:
            self.image = tile_images['wall']
            bullet_stopper_group.remove(self)
            walls_group.add(self)
        elif self.cond == 2:
            self.image = tile_images['empty']
            walls_group.remove(self)


class Hole(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, hole_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class ShopItem(pygame.sprite.Sprite):
    def __init__(self, type, pos_x, pos_y):
        super().__init__(shop_items_group, all_sprites)
        self.image = load_image('images\\{}.png'.format(type), -1)
        self.item_type = type
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.rect.x + self.dx
        obj.rect.y = obj.rect.y + self.dy
        if type(obj) in [Enemy, Bullet]:
            obj.sx += self.dx
            obj.sy += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def reset_groups():
    tiles_group.empty()
    player_group.empty()
    walls_group.empty()
    all_sprites.empty()
    hole_group.empty()
    bullet_group.empty()
    enemy_group.empty()
    dead_group.empty()
    bullet_stopper_group.empty()
    temp_walls_group.empty()
    gold_text_group.empty()
    shop_items_group.empty()
    shop_text_group.empty()


def load_level(level):
    with open('data/levels/' + level, 'r') as mapFile:
        level_map = [list(line.strip()) for line in mapFile]
    return list(level_map)


def draw_room(level, i, j, t):
    global player, sig
    if t == 'room':
        ax = 0
        ay = 0
    elif t == 'hor':
        ax = 15
        ay = 5
    else:
        ax = 5
        ay = 15
    for y in range(len(level)):
        for x in range(len(level[0])):
            if level[x][y] == '.':
                Tile('empty', x + j * 20 + ax, y + i * 20 + ay)
            elif level[x][y] == '#':
                Wall('wall', x + j * 20 + ax, y + i * 20 + ay)
            elif level[x][y] == '@':
                Tile('empty', x + j * 20, y + i * 20)
                player = Player(x + j * 20, y + i * 20)
            elif level[x][y] == '$':
                Hole('hole', x + j * 20, y + i * 20)
            elif level[x][y] == '%':
                Tile('empty', x + j * 20, y + i * 20)
                Enemy(x + j * 20, y + i * 20)
            elif level[x][y] == ':':
                level_map[i][j][3].append(TempWall(x + j * 20, y + i * 20))
    if level_map[i][j][0] == 'shop' and t == 'room':
        sig = []
        ShopItem('heart', 3 + j * 20, 7 + i * 20)
        sig.append(GoldText(3 + j * 20, 8.5 + i * 20, '300', 'shop'))
        n = randint(0, 3)
        ShopItem(weapon_names[n][0], 9 + j * 20, 7 + i * 20)
        sig.append(GoldText(9 + j * 20, 8.5 + i * 20, str(weapon_names[n][1]), 'shop'))


def draw_level():
    global level_map
    names = level_names
    shuffle(names)
    k = randint(5, 7)
    names = names[:k]
    names.append('shop')
    shuffle(names)
    k += 1
    level_map = []
    for i in range(9):
        level_map.append([''] * 9)
    level_map[3][3] = 'start'
    names.append('end')
    n = 0
    while n <= k:
        x, y = randint(1, 7), randint(1, 7)
        if (level_map[y + 1][x] != '' or level_map[y - 1][x] != '' or level_map[y][x + 1] != '' or
            level_map[y][x - 1] != '') and level_map[y][x] == '':
            level_map[y][x] = names[n]
            n += 1
    hor = load_level('hor_corridor.txt')
    vert = load_level('vert_corridor.txt')
    for i in range(len(level_map)):
        for j in range(len(level_map[0])):
            if level_map[i][j] != '':
                ea = level_map[i][j] not in ['start', 'end', 'shop']
                level = load_level(level_map[i][j] + '.txt')
                nel = ne = randint(3, 5)
                while ne > 0 and ea:
                    x = randint(1, 14)
                    y = randint(1, 14)
                    if level[x][y] == '.' and enemies_allowed[x][y]:
                        level[x][y] = '%'
                        ne -= 1
                symb = ':' if ea else '.'
                if ea:
                    level_map[i][j] = [level_map[i][j], nel, 'full', []]
                else:
                    level_map[i][j] = [level_map[i][j], 0, 'main', []]
                if level_map[i + 1][j] != '':
                    level[6][14] = symb
                    level[7][14] = symb
                    level[8][14] = symb
                    draw_room(hor, i, j, 'vert')
                if level_map[i - 1][j] != '':
                    level[6][0] = symb
                    level[7][0] = symb
                    level[8][0] = symb
                if level_map[i][j + 1] != '':
                    level[14][6] = symb
                    level[14][7] = symb
                    level[14][8] = symb
                    draw_room(vert, i, j, 'hor')
                if level_map[i][j - 1] != '':
                    level[0][6] = symb
                    level[0][7] = symb
                    level[0][8] = symb
                draw_room(level, i, j, 'room')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        num = randint(0, 2)
        name = enemy_pics[num]
        self.image = load_image(f'images\\{name}', -1)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.direction = 'right'
        self.walk_cycle = 0
        self.v = 1.5
        self.sx, self.sy = self.rect.center
        self.hp = 20 * 1.2 ** (floor - 1)
        self.room = [pos_x // 20, pos_y // 20]
        self.a = 256
        self.drop = [8, 12]
        self.killed = False

    def update(self):
        if self.hp > 0:
            if self.room == player.room and not player.in_corridor:
                x, y = player.rect.center
                g = ((x - self.sx) ** 2 + (self.sy - y) ** 2) ** 0.5
                if g != 0:
                    vx = (x - self.sx) / g * self.v
                    vy = (y - self.sy) / g * self.v
                else:
                    vx, vy = 0, 0
                self.sx, self.sy = self.sx + vx, self.sy + vy
                self.rect.center = (self.sx, self.sy)
                if pygame.sprite.spritecollideany(self, walls_group):
                    fvx = self.v if vx >= 0 else -self.v
                    fvy = self.v if vy >= 0 else -self.v
                    self.sx = self.sx - vx
                    self.sy = self.sy - vy + fvy
                    self.rect.center = (self.sx, self.sy)
                    if pygame.sprite.spritecollideany(self, walls_group):
                        self.sx, self.sy = self.sx + fvx, self.sy - fvy
                        self.rect.center = (self.sx, self.sy)
                        if pygame.sprite.spritecollideany(self, walls_group):
                            self.sx = self.sx - fvx
                            self.rect.center = (self.sx, self.sy)
        else:
            if self.a == 256:
                enemy_group.remove(self)
                dead_group.add(self)
                drop = randint(self.drop[0], self.drop[1])
                player.gold += drop
                GoldText(self.rect.left, self.rect.top, drop, 'death')
            if self.a > 0:
                self.a -= 5
                self.image.set_alpha(self.a)
            else:
                self.kill()


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
        self.gun = Blaster(self.rect.left, self.rect.top)

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
        x = int(983 / 1920 * infoObject.current_w)
        y = int(560 / 1080 * infoObject.current_h)
        self.rect = self.image.get_rect(center=(x, y))


class Blaster(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\blaster.png', -1)
        self.image = load_image('images\\blaster.png', -1)
        self.bv = 10
        self.damage = 5
        self.gap = 20

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 30)
        self.sound = load_music('shoot.mp3')


class Minigun(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\minigun.png', -1)
        self.image = load_image('images\\minigun.png', -1)
        self.bv = 30
        self.damage = 15
        self.gap = 30

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 100)
        self.sound = load_music('shoot_2.mp3')


class Pistol(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\pistol.png', -1)
        self.image = load_image('images\\pistol.png', -1)
        self.bv = 20
        self.damage = 10
        self.gap = 7

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 20)
        self.sound = load_music('shoot_2.mp3')


class SBC(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\sbc.png', -1)
        self.image = load_image('images\\sbc.png', -1)
        self.bv = 20
        self.damage = 5
        self.gap = 2

    def shoot(self, pos):
        Bullet(pos[0], pos[1], self.bv, self.damage, 15)
        self.sound = load_music('shoot_2.mp3')


class BFG9000(Gun):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.normal_image = load_image('images\\bfg9000.png', -1)
        self.image = load_image('images\\bfg9000.png', -1)
        self.bv = 15
        self.damage = 10
        self.gap = 60

    def shoot(self, pos):
        for i in range(10):
            Bullet(pos[0], pos[1], self.bv, self.damage, 10)
            self.sound = load_music('shoot_3.mp3')


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


class GoldText(pygame.sprite.Sprite):
    def __init__(self, x, y, gold, text_type):
        if text_type == 'shop':
            super().__init__(shop_text_group, all_sprites)
            x *= tile_width
            y *= tile_height
        elif text_type == 'death':
            super().__init__(gold_text_group, all_sprites)
        self.image = pygame.font.Font(None, 40).render(str(gold), 1, pygame.Color('yellow'))
        self.rect = self.image.get_rect().move(x + 7, y - 30)
        self.x = 0

    def update(self):
        self.rect.top -= 1
        self.x += 1
        if self.x > 70:
            self.kill()


class MiniRoom(pygame.sprite.Sprite):
    def __init__(self, x, y, group, room_type, room_cond):
        super().__init__(group)
        image = 'mini_room'
        if room_cond == 'main':
            if room_type == 'shop':
                image += '_coin'
            elif room_type == 'start':
                image += '_start'
            elif room_type == 'end':
                image += '_end'
        elif room_cond == 'running':
            image += '_running'
        elif room_cond == 'cleared':
            image += '_cleared'
        if [x, y] == player.room:
            image += '_current'
        self.image = load_image('images\\' + image + '.png')
        self.rect = self.image.get_rect().move(x * 150, y * 150)


class Menu:
    def __init__(self):
        self.in_menu = True
        self.run_menu()

    def draw_menu(self):
        pygame.mouse.set_visible(True)
        screen = pygame.display.set_mode((width, height))
        screen.fill(pygame.Color('black'))
        screen.blit(load_image('images\\menu_background.png'), (0, 0))
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 3, height // 3, width // 3, height // 6), 5)
        pygame.draw.rect(screen, pygame.Color('red'),
                         (width // 3, height // 3 * 2, width // 3, height // 6), 5)
        size_1 = int(220 / 1920 * infoObject.current_w)
        place_1 = int(350 / 1920 * infoObject.current_w)
        font = pygame.font.Font('data\\fonts\\BAUHS93.TTF', size_1)
        screen.blit(font.render("Space Shoot", 1, pygame.Color('red')),
                    (place_1, 10))
        size_2 = int(120 / 1920 * infoObject.current_w)
        place_2 = int(120 / 1920 * infoObject.current_w)
        font = pygame.font.Font('data\\fonts\\comic.ttf', size_2)
        screen.blit(font.render("Играть", 1, pygame.Color('red')),
                    (width // 3 + place_2, height // 3 - 10))
        screen.blit(font.render("Выход", 1, pygame.Color('red')),
                    (width // 3 + place_2, height // 3 * 2 - 10))

    def run_menu(self):
        global in_game
        self.draw_menu()
        load_menu_music()
        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.in_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] in range(width // 3, width // 3 * 2):
                        if event.pos[1] in range(height // 3, height // 2):
                            self.in_menu = False
                            in_game = True
                        elif event.pos[1] in range(height // 3 * 2, height // 6 * 5):
                            self.in_menu = False
            clock.tick(fps)
            pygame.display.flip()


def death_anim():
    global dead, player
    a = 255
    screen_sprite_group = pygame.sprite.Group()
    screen_sprite = pygame.sprite.Sprite(screen_sprite_group)
    screen_sprite.image = load_image('images\\screen.png').convert()
    screen_sprite.rect = screen_sprite.image.get_rect()
    load_music('game_over.mp3')
    while dead:
        screen.fill(pygame.Color('white'))
        screen_sprite.image.set_alpha(a)
        screen_sprite_group.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        if a <= 0:
            player.gun.kill()
            player.kill()
            dead = False
            menu.in_menu = True
        a -= 2


def generate_map():
    global floor
    reset_groups()
    draw_level()
    floor += 1


def run_map():
    mini_room_group = pygame.sprite.Group()
    in_map = True
    timer = 0
    for i in range(9):
        for j in range(9):
            if level_map[i][j] != '':
                MiniRoom(j, i, mini_room_group, level_map[i][j][0], level_map[i][j][2])
    while in_map:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and timer > 60:
                    in_map = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    for s in mini_room_group:
                        s.rect.left -= 5
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for s in mini_room_group:
                        s.rect.left += 5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    for s in mini_room_group:
                        s.rect.top += 5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    for s in mini_room_group:
                        s.rect.top -= 5
        screen.fill(pygame.Color('black'))
        mini_room_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        timer += 1


def run_escape():
    global in_game
    mouse_pos = (0, 0)
    in_pause = True
    timer = 60
    image = load_image('images\\screen.png')
    while in_pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and timer == 0:
                    in_pause = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(width // 4 + 204, (width // 4 + 204) + (width // 2 - 388)):
                    if event.pos[1] in range(height // 4 + 80, height // 4 + 220):
                        in_pause = False
                    elif event.pos[1] in range(height // 4 + 280, height // 4 + 420):
                        player.gun.kill()
                        player.kill()
                        in_pause = False
                        in_game = False
                        menu.in_menu = True
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, pygame.Color('brown'),
                         (width // 4, height // 4, width // 2, height // 2), 40)
        pygame.draw.rect(screen, pygame.Color('white'),
                         (width // 4 + 20, height // 4 + 20, width // 2 - 40, height // 2 - 40), 0)
        pygame.draw.rect(screen, pygame.Color('brown'),
                         (width // 4 + 204, height // 4 + 80, width // 2 - 388, 100), 5)
        pygame.draw.rect(screen, pygame.Color('brown'),
                         (width // 4 + 204, height // 4 + 280, width // 2 - 388, 100), 5)
        side = int(60 / 1920 * infoObject.current_w)
        font = pygame.font.Font(None, side)
        screen.blit(font.render("Вернуться в игру", 1, pygame.Color('brown')),
                    (width // 4 + 224, height // 4 + 120))
        screen.blit(font.render("Выйти в меню", 1, pygame.Color('brown')),
                    (width // 4 + 224, height // 4 + 320))
        screen.blit(arrow, mouse_pos)
        clock.tick(fps)
        pygame.display.flip()
        if timer > 0:
            timer -= 1


def run_game():
    global screen, in_game, dead, floor
    floor = 0
    mouse_pos = (0, 0)
    camera = Camera()
    screen = pygame.display.set_mode((width, height))
    generate_map()
    pygame.mouse.set_visible(False)
    damage_timer = 0
    shoot_timer = 0
    map_timer = 0
    escape_timer = 0
    shooting = False
    background_music()
    while in_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                shooting = False
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                player.gun.rotate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.move(0, 1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(0, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player.png', -1)
                    else:
                        player.image = load_image('images\\player_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'right'
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.move(0, -1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(0, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_left.png', -1)
                    else:
                        player.image = load_image('images\\player_left_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'left'
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.move(1, -1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(1, 1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_back.png', -1)
                    else:
                        player.image = load_image('images\\player_back_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'up'
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.move(1, 1)
                    if pygame.sprite.spritecollideany(player.hitbox, walls_group):
                        player.move(1, -1)
                    if player.walk_cycle < 10:
                        player.image = load_image('images\\player_front.png', -1)
                    else:
                        player.image = load_image('images\\player_front_2.png', -1)
                    player.walk_cycle = (player.walk_cycle + 1) % 20
                    player.direction = 'down'
                if event.key == pygame.K_m and map_timer == 0:
                    run_map()
                    map_timer = 60
                if event.key == pygame.K_ESCAPE and escape_timer == 0:
                    pygame.image.save(screen, 'data\\images\\screen.png')
                    run_escape()
                    escape_timer = 60
                if pygame.sprite.spritecollideany(player.hitbox, hole_group):
                    hp = player.hp
                    gold = player.gold
                    gun = player.gun
                    generate_map()
                    player.hp = hp
                    player.gold = gold
                    player.gun = gun
        rx, ry = player.room[0], player.room[1]
        if level_map[ry][rx] != '' and not player.in_corridor:
            if level_map[ry][rx][2] == 'full':
                level_map[ry][rx][2] = 'running'
                for sprite in level_map[ry][rx][3]:
                    sprite.update()
            elif level_map[ry][rx][2] == 'running' and level_map[ry][rx][1] == 0:
                level_map[ry][rx][2] = 'cleared'
                for sprite in level_map[ry][rx][3]:
                    sprite.update()
        if shooting:
            if shoot_timer == 0:
                player.gun.shoot(mouse_pos)
                shoot_timer = player.gun.gap
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        font = pygame.font.Font(None, 55)
        clock.tick(fps)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        temp_walls_group.draw(screen)
        dead_group.update()
        enemy_group.update()
        bullet_group.update()
        collide = pygame.sprite.groupcollide(bullet_group, enemy_group, True, False)
        for i in range(len(collide)):
            keys = list(collide.keys())
            damage = keys[i].damage
            for j in collide[keys[i]]:
                if not player.in_corridor:
                    j.hp -= damage
                if j.hp <= 0 and not j.killed:
                    level_map[ry][rx][1] -= 1
                    j.killed = True
                    player.gold += randint(j.drop[0], j.drop[1])
        bought = False
        collide = pygame.sprite.groupcollide(player_group, shop_items_group, False, False)
        if collide:
            key = list(collide.keys())[0]
            if collide[key][0].item_type == 'heart':
                bought = player.gold >= 300
                if bought:
                    player.hp += 1
                    sig[0].kill()
                    player.gold -= 300
            else:
                if collide[key][0].item_type == 'minigun' and \
                        player.gun != Minigun(player.rect.left, player.rect.top):
                    bought = player.gold >= 200
                    if bought:
                        player.gun.kill()
                        player.gun = Minigun(player.rect.left, player.rect.top)
                        player.gold -= 200
                elif collide[key][0].item_type == 'pistol' \
                        and player.gun != Pistol(player.rect.left, player.rect.top):
                    bought = player.gold >= 300
                    if bought:
                        player.gun.kill()
                        player.gun = Pistol(player.rect.left, player.rect.top)
                        player.gold -= 300
                elif collide[key][0].item_type == 'sbc'\
                        and player.gun != SBC(player.rect.left, player.rect.top):
                    bought = player.gold >= 500
                    if bought:
                        player.gun.kill()
                        player.gun = SBC(player.rect.left, player.rect.top)
                        player.gold -= 500
                elif collide[key][0].item_type == 'bfg9000'\
                        and player.gun != BFG9000(player.rect.left, player.rect.top):
                    bought = player.gold >= 650
                    if bought:
                        player.gun.kill()
                        player.gun = BFG9000(player.rect.left, player.rect.top)
                        player.gold -= 650
                if bought:
                    sig[-1].kill()
            if bought:
                collide[key][0].kill()
        enemy_group.draw(screen)
        dead_group.draw(screen)
        if player.direction == 'up':
            gun_group.draw(screen)
            player_group.draw(screen)
        else:
            player_group.draw(screen)
            gun_group.draw(screen)
        pygame.sprite.groupcollide(bullet_group, walls_group, True, False)
        pygame.sprite.groupcollide(bullet_group, bullet_stopper_group, True, False)
        bullet_group.draw(screen)
        screen.blit(font.render("Этаж " + str(floor), 1, pygame.Color('red')), (1730, 20))
        screen.blit(font.render(str(player.gold), 1, pygame.Color('yellow')), (30, 100))
        screen.blit(load_image('images\\coin.png', -1), (30 + 23 * len(str(player.gold)), 95))
        if pygame.sprite.spritecollideany(player.hitbox, enemy_group) and damage_timer == 0:
            player.hp -= 1
            damage_timer = 120
        gold_text_group.update()
        gold_text_group.draw(screen)
        shop_text_group.draw(screen)
        shop_items_group.draw(screen)
        n = 20
        for i in range(player.hp):
            screen.blit(load_image('images\\heart.png', -1), (n, 20))
            n += 84
        if player.hp <= 0:
            pygame.image.save(screen, 'data\\images\\screen.png')
            in_game = False
            dead = True
        screen.blit(arrow, mouse_pos)
        pygame.display.flip()
        if damage_timer > 0:
            damage_timer -= 1
        if shoot_timer > 0:
            shoot_timer -= 1
        if map_timer > 0:
            map_timer -= 1
        if escape_timer > 0:
            escape_timer -= 1


pygame.init()
infoObject = pygame.display.Info()
width, height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60
level_names = ['room1', 'room2', 'room3', 'room4', 'room5', 'room6', 'room7', 'room8', 'room9',
               'room10']
weapon_names = [['minigun', 200], ['pistol', 300], ['sbc', 500], ['bfg9000', 650]]
enemy_pics = ['monster.png', 'monster2.png', 'monster3.png']
room_map = []
enemies_allowed = []
for i in range(15):
    enemies_allowed.append([])
    for j in range(15):
        enemies_allowed[i].append(True)
for i in range(5, 10):
    enemies_allowed[0][i] = False
    enemies_allowed[1][i] = False
    enemies_allowed[2][i] = False
    enemies_allowed[12][i] = False
    enemies_allowed[13][i] = False
    enemies_allowed[14][i] = False
    enemies_allowed[i][0] = False
    enemies_allowed[i][1] = False
    enemies_allowed[i][2] = False
    enemies_allowed[i][12] = False
    enemies_allowed[i][13] = False
    enemies_allowed[i][14] = False
dead = False
in_game = False
floor = 0
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
gun_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
dead_group = pygame.sprite.Group()
gold_text_group = pygame.sprite.Group()
shop_text_group = pygame.sprite.Group()
bullet_stopper_group = pygame.sprite.Group()
temp_walls_group = pygame.sprite.Group()
hole_group = pygame.sprite.Group()
shop_items_group = pygame.sprite.Group()
tile_images = {'wall': load_image('images\\wall.png'),
               'empty': load_image('images\\floor.png'),
               'hole': load_image('images\\hole.png')}
tile_width = 64
tile_height = 64
mw = 15
mh = 15
arrow = load_image('images\\scope.png', -1)
menu = Menu()
while in_game or menu.in_menu or dead:
    if in_game:
        run_game()
    if menu.in_menu:
        menu.run_menu()
    if dead:
        death_anim()
