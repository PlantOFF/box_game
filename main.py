import sys
import os
from time import time

import sqlite3
import pygame
from random import choice

# Старт приложения и констант для работы приложения
pygame.init()
FPS = 3
SIZE = WIDTH, HEIGHT = 500, 500
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
# одключение БД
con = sqlite3.connect("UserData")
cur = con.cursor()
# оздание групп для спрайтов
hud_sprites = pygame.sprite.Group()
fighter_sprites = pygame.sprite.Group()


# Здоровье Игрока
class Player_hp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(hud_sprites)
        self.hp = 100
        self.image = load_image('hp_bar_player.png', resize=[200, 25])
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(20, 30)

    def update(self):
        pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(screen, (0, 0, 0),
                         (220 - 200 * ((100 - self.hp) / 100), 30, 220 * ((100 - self.hp) / 100), 25))


# Здоровье врага
class Fighter_hp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(hud_sprites)
        self.hp = 100
        self.image = load_image('hp_bar_fighter.png', resize=[200, 25])
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(260, 30)

    def update(self):
        pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        pygame.draw.rect(screen, (0, 0, 0),
                         (260, 30, 200 * ((100 - self.hp) / 100), 25))


# Правая рука
class Arm_r(pygame.sprite.Sprite):
    def __init__(self, columns):
        super().__init__(hud_sprites)
        self.action = 'idle'
        self.frames = []
        self.cut_sheet(columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(250, 250)

    def cut_sheet(self, columns):
        if self.action == 'idle':
            sheet = load_image('arm_r.png', colorkey=-1, resize=[380, 380])
        elif self.action == 'block':
            sheet = load_image('block_r.png', colorkey=-1, resize=[380, 380])
        else:
            sheet = load_image('punch_r.png', colorkey=-1, resize=[380, 380])

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height())

        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Левая рука
class Arm_l(pygame.sprite.Sprite):
    def __init__(self, columns):
        super().__init__(hud_sprites)
        self.action = 'idle'
        self.frames = []
        self.cut_sheet(columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(50, 250)

    def cut_sheet(self, columns):
        if self.action == 'idle':
            sheet = load_image('arm_l.png', colorkey=-1, resize=[380, 380])
        elif self.action == 'block':
            sheet = load_image('block_l.png', colorkey=-1, resize=[380, 380])
        else:
            sheet = load_image('punch_l.png', colorkey=-1, resize=[380, 380])

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height())

        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Соперник
class Fighter(pygame.sprite.Sprite):
    def __init__(self, number, columns, resize=(380, 380)):
        super().__init__(fighter_sprites)
        self.number = number
        self.action = 'idle'
        self.frames = []
        self.cut_sheet(columns, resize)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(175, 150)

    def choose_action(self):
        match self.number:
            case 1:
                return choice(['punch', 'block', 'idle', 'idle'])
            case 2:
                return choice(['punch', 'block', 'block', 'block', 'block', 'idle'])
            case 3:
                return choice(['punch', 'punch', 'punch', 'punch', 'punch', 'block', 'block', 'idle'])

    def cut_sheet(self, columns, resize=(380, 380)):
        if self.action == 'idle':
            sheet = load_image(f'idle_boxer{self.number}.png', colorkey=-1, resize=resize)
        elif self.action == 'block':
            sheet = load_image(f'block_boxer{self.number}.png', colorkey=-1, resize=resize)
        elif self.action == 'loose':
            sheet = load_image(f'loose_boxer{self.number}.png', colorkey=-1, resize=resize)
        else:
            sheet = load_image(f'punch_boxer{self.number}.png', colorkey=-1, resize=resize)

        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height())

        for i in range(columns):
            frame_location = (self.rect.w * i, 0)
            self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Загрузка изображения
def load_image(name, colorkey=None, resize=None):
    fullname = os.path.join('data', name)

    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    if resize is not None:
        image = pygame.transform.scale(image, (resize[0], resize[1]))

    return image


# Создание всех спрайтов
arm_left = Arm_l(2)
arm_right = Arm_r(2)
fighter = Fighter(1, 2, [250, 250])
player_hp = Player_hp()
fighter_hp = Fighter_hp()


# Завершение программы
def terminate():
    pygame.quit()
    sys.exit()


# Стартовые экран
def start_screen():
    intro_text = ["                         ЖЁСТКИЙ БОКС", "",
                  "Управление:",
                  "Q - удар левой",
                  "W - блок",
                  "E - удар правой",
                  "", "НАЖМИТЕ ЛЮБУЮ КЛАВИШУ ЧТОБЫ НАЧАТЬ"]

    fon = pygame.transform.scale(load_image('tutor.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                choose_screen()

        pygame.display.flip()
        clock.tick(FPS)


# Режим выживание
def death_match():
    enemy_hp = 100
    current_hp = 100
    start_time = time()
    count = 0
    fon = pygame.transform.scale(load_image('ring.jpg'), (WIDTH, HEIGHT))

    while True:
        if fighter.action == 'punch' and arm_left.action != 'block':
            current_hp -= choice(range(1, 5))
        default(arm_left, arm_right)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_e]:
                arm_right.cur_frame = 1
                right_punch(arm_right)

                if fighter.action != 'block':
                    enemy_hp -= choice(range(1, 5))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_q]:
                arm_left.cur_frame = 1
                left_punch(arm_left)

                if fighter.action != 'block':
                    enemy_hp -= choice(range(1, 5))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_w]:
                arm_right.cur_frame = 1
                arm_left.cur_frame = 1
                block(arm_left, arm_right)
        if current_hp <= 0:
            end_time = time()
            score = int((end_time - start_time) * 100)
            end_screen(score, 'проиграли!')
        elif enemy_hp <= 0:
            enemy_hp = 0
            fighter.number = choice([1, 2, 3])
            fighter.action = 'loose'
            fighter.frames = []
            fighter.cut_sheet(2)
            fighter.rect = fighter.rect.move(165, 150)
            count += 1

            if count == 12:
                count = 0
                enemy_hp = 100
                fighter.action = 'idle'
                fighter.frames = []
                fighter.cut_sheet(2)
                fighter.rect = fighter.rect.move(165, 150)

        screen.blit(fon, (0, 0))
        fighter_hp.hp = enemy_hp
        player_hp.hp = current_hp
        fighter_actions(fighter)
        fighter_sprites.draw(screen)
        hud_sprites.draw(screen)
        hud_sprites.update()
        fighter_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


# Экран выбора соперников
def choose_screen():
    intro_text = ["                         ЖЁСТКИЙ БОКС", "", "", "", "", "", "", "", "",
                  "                      Выберите соперника",
                  "                            Нажимайте 1-3",
                  "                              Выживание"]

    while True:
        fon = pygame.transform.scale(load_image('tutor.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, (35, 168, 164), (180, 440, 135, 25))
        screen_words(intro_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_1]:
                fighter.number = 1
                fighter.frames = []
                fighter.cut_sheet(2, (250, 250))
                fighter.rect = fighter.rect.move(175, 150)
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_2]:
                fighter.number = 2
                fighter.frames = []
                fighter.cut_sheet(2, (250, 250))
                fighter.rect = fighter.rect.move(175, 150)
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_3]:
                fighter.number = 3
                fighter.frames = []
                fighter.cut_sheet(2, (250, 250))
                fighter.rect = fighter.rect.move(175, 150)
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                generate_fight(fighter)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (
                    180 <= pygame.mouse.get_pos()[0] <= 315 and 440 <= pygame.mouse.get_pos()[1] <= 465):
                death_match()

        fighter_sprites.update()
        fighter_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Сброс всех действий при новом
def default(arm_left, arm_right):
    arm_left.action = 'idle'
    arm_right.action = 'idle'
    arm_left.cut_sheet(2)
    arm_left.rect = arm_left.rect.move(50, 250)
    arm_right.cut_sheet(2)
    arm_right.rect = arm_right.rect.move(250, 250)


# Левый удар
def left_punch(arm_left):
    arm_left.action = 'punch'
    arm_left.frames = []
    arm_left.cut_sheet(2)
    arm_left.rect = arm_left.rect.move(50, 250)


# Правый удар
def right_punch(arm_right):
    arm_right.action = 'punch'
    arm_right.frames = []
    arm_right.cut_sheet(2)
    arm_right.rect = arm_right.rect.move(250, 250)


# Блок
def block(arm_left, arm_right):
    arm_left.action = 'block'
    arm_right.action = 'block'
    arm_left.frames = []
    arm_right.frames = []
    arm_left.cut_sheet(2)
    arm_right.cut_sheet(2)
    arm_left.rect = arm_left.rect.move(100, 175)
    arm_right.rect = arm_right.rect.move(200, 175)


# Смена текущего действия для соперника
def fighter_actions(fighter):
    if fighter.action != 'loose':
        fighter.action = fighter.choose_action()
        fighter.cut_sheet(2)
        fighter.rect = fighter.rect.move(165, 150)


# Вывод заданного текста на экран
def screen_words(intro_text, text_coords=100):
    font = pygame.font.Font(None, 30)
    text_coord = text_coords

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


# Поиск данных в БД для таблицы лидеров
def generate_leaderboard():
    result = sorted(cur.execute("""SELECT * FROM LeaderBoard""").fetchall(), key=lambda x: x[1], reverse=True)
    input_text = []
    count = 0

    for user in result:
        if count == 7:
            break
        input_text.append('               ' + user[0] + '    ' + str(user[1]))
        count += 1

    screen_words(input_text, 160)
    con.commit()


# Вывод данных таблицы лидеров
def leaderboard(score):
    is_confirmed = False
    name = ''
    intro_text = [
        "                      ТАБЛИЦА ЛИДЕРОВ",
        "               Имя                                   Счёт", "", "", "", "", "", "", "",
        "Введите имя:   "
    ]

    fon = pygame.transform.scale(load_image('tutor.jpg'), (WIDTH, HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if is_confirmed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                    and (155 <= pygame.mouse.get_pos()[0] <= 340 and 375 <= pygame.mouse.get_pos()[1] <= 405):
                fighter.action = 'idle'
                fighter.frames = []
                fighter.cut_sheet(2, (250, 250))
                fighter.rect = fighter.rect.move(175, 150)
                start_screen()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                cur.execute(f"""
                INSERT INTO LeaderBoard VALUES('{name}', {score}) 
                """)
                intro_text[-1] = ''
                is_confirmed = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    intro_text[-1] = intro_text[-1][:-1]
                    name = name[:-1]
                elif len(intro_text[-1]) < 32:
                    intro_text[-1] += event.unicode
                    name += event.unicode

                    if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RETURN]:
                        intro_text[-1] = intro_text[-1][:-1]
                        name = name[:-1]
        screen.blit(fon, (0, 0))

        if not is_confirmed:
            pygame.draw.rect(screen, (35, 168, 164), (155, 375, 250, 30))
        else:
            intro_text[-1] = '                            Главное меню'
            pygame.draw.rect(screen, (35, 168, 164), (155, 375, 185, 30))

        screen_words(intro_text)
        generate_leaderboard()
        pygame.display.flip()
        clock.tick(FPS)


# Экран окончания игры
def end_screen(score, end):
    intro_text = ["ЖЁСТКИЙ БОКС", "",
                  f"Вы {end}",
                  f"Вы набрали {score} очков!",
                  "",
                  "",
                  "Удачи в следующей игре!",
                  "",
                  "",
                  "                      Сохранить результаты"]

    fon = pygame.transform.scale(load_image('tutor.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                    and (125 <= pygame.mouse.get_pos()[0] <= 375 and 375 <= pygame.mouse.get_pos()[1] <= 405):
                leaderboard(score)

        pygame.draw.rect(screen, (35, 168, 164), (125, 375, 250, 30))
        screen_words(intro_text)
        pygame.display.flip()
        clock.tick(FPS)


# Генерация боя
def generate_fight(fighter):
    enemy_hp = 100
    current_hp = 100
    start_time = time()
    count = 0
    fon = pygame.transform.scale(load_image('ring.jpg'), (WIDTH, HEIGHT))

    while True:
        if fighter.action == 'punch' and arm_left.action != 'block':
            current_hp -= choice(range(1, 5))
        default(arm_left, arm_right)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_e]:
                arm_right.cur_frame = 1
                right_punch(arm_right)

                if fighter.action != 'block':
                    enemy_hp -= choice(range(1, 5))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_q]:
                arm_left.cur_frame = 1
                left_punch(arm_left)

                if fighter.action != 'block':
                    enemy_hp -= choice(range(1, 5))
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_w]:
                arm_right.cur_frame = 1
                arm_left.cur_frame = 1
                block(arm_left, arm_right)
        if current_hp <= 0:
            end_time = time()
            score = int((end_time - start_time) * 100)
            end_screen(score, 'проиграли!')
        elif enemy_hp <= 0:
            enemy_hp = 0
            end_time = time()
            score = int((end_time - start_time) * 100)
            fighter.action = 'loose'
            fighter.frames = []
            fighter.cut_sheet(2)
            fighter.rect = fighter.rect.move(165, 150)
            count += 1

            if count == 12:
                end_screen(score, 'выиграли!')

        screen.blit(fon, (0, 0))
        fighter_hp.hp = enemy_hp
        player_hp.hp = current_hp
        fighter_actions(fighter)
        fighter_sprites.draw(screen)
        hud_sprites.draw(screen)
        hud_sprites.update()
        fighter_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
