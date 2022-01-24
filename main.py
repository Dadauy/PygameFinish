from typing import Tuple

import pygame
from pygame.sprite import AbstractGroup

# словарь с цветом его rgb
colors = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BLACK": (0, 0, 0),
    "GREY": (105, 105, 105),
    "YELLOW": (255, 255, 0),
    "BROWN": (171, 106, 79),
}

pygame.init()


class Camera:
    """Камера
    Она следует строго за персонажем"""

    def __init__(self, pos: Tuple[int, int]):
        self._pos = pygame.Vector2(*pos)

    @property
    def pos(self) -> Tuple[float, float]:
        return self._pos.x, self._pos.y

    @pos.setter
    def pos(self, pos: Tuple[float, float]):
        self._pos[0] = pos[0]
        self._pos[1] = pos[1]

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, v):
        self._pos.x = v

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, v):
        self._pos.y = v


class Player(pygame.sprite.Sprite):
    """Персонаж
    Он может двигаться во все 4 сторноны
    Изменение его спрайта
    Здоровье персонажа"""

    def __init__(self, camera: Camera, *groups: AbstractGroup):
        super().__init__(*groups)

        self.right = False  # флаг отвечающий за движение вправо
        self.left = False  # флаг отвечающий за движение влево
        self.stop = True  # флаг отвеяающий за покой
        self.cur_frame = 0

        self.hp_player = 100  # жизни персонажа

        self.size = (19, 34)  # размер персонажа
        self.image = pygame.Surface(self.size)

        self.rect = pygame.Rect((32, 32), self.size)  # появление персонажа
        self.camera = camera

        self.right_or_left = "./data/automaton.png"  # ссылка на спрайт с автоматом

    def cord(self):
        """координаты персонажа"""
        return self.rect.x, self.rect.y

    def health(self):
        """здоровье персонажа"""
        pygame.draw.rect(display, (255, 255, 255), (10, 10, 100, 20), 2)  # рисуется контур который обозначает все жизни
        pygame.draw.rect(display, (0, 255, 0), (12, 12, 0.96 * self.hp_player, 16))  # рисуется полоса жизни

    def move(self, c_x, c_y):
        """передвижение персонажа"""
        STEP = 3

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # движение вверх по монитору
            self.rect.y -= STEP
            c_y += STEP

            self.left = False
            self.stop = True
            self.right = False

        if keys[pygame.K_s]:  # движение ввниз по монитору
            self.rect.y += STEP
            c_y -= STEP

            self.left = False
            self.stop = True
            self.right = False

        if keys[pygame.K_a]:  # движение влево по монитору
            self.rect.x -= STEP
            c_x += STEP

            self.left = True
            self.stop = False
            self.right = False

        if keys[pygame.K_d]:  # движение вправо по монитору
            self.rect.x += STEP
            c_x -= STEP

            self.left = False
            self.stop = False
            self.right = True

        return c_x, c_y

    def update(self, *args, **kwargs) -> None:
        self.health()  # обновление полосы жизней

        camera_pos_x, camera_pos_y = self.camera.pos  # координаты камеры
        old_player_pos = self.rect.x, self.rect.y  # координаты персонажа

        new_c_x, new_c_y = self.move(camera_pos_x, camera_pos_y)  # новые координаты камеры

        if pygame.sprite.spritecollideany(self, blocks_wall):  # если персонаж столкнулся со стеной, то его движение
            # не изменяется
            self.rect.x, self.rect.y = old_player_pos
            return

        #  изменение спрайтов
        PERIOD_SPRITE = 60
        PERIOD_LEFT_OR_RIGTH = 30
        if self.stop:
            self.image = pygame.image.load("./data/human/idle.gif")
        if self.left:
            self.right_or_left = "./data/automaton_left.png"
            if self.rect.x % PERIOD_SPRITE >= PERIOD_LEFT_OR_RIGTH:
                self.image = pygame.image.load("./data/human/run_left.png")
            elif self.rect.x % PERIOD_SPRITE <= PERIOD_LEFT_OR_RIGTH:
                self.image = pygame.image.load("./data/human/idle_left.png")
        if self.right:
            self.right_or_left = "./data/automaton.png"
            if self.rect.x % PERIOD_SPRITE >= PERIOD_LEFT_OR_RIGTH:
                self.image = pygame.image.load("./data/human/run.gif")
            elif self.rect.x % PERIOD_SPRITE <= PERIOD_LEFT_OR_RIGTH:
                self.image = pygame.image.load("./data/human/idle.gif")

        automaton.image = pygame.image.load(self.right_or_left)  # загрузка автомата
        self.camera.pos = new_c_x, new_c_y  # координаты камеры


class Bullet(pygame.sprite.Sprite):
    """Пули
    Движение пули
    Уничтожение пули при столкновений"""

    def __init__(self, name, pos, speed, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] + 16  # чтобы пуля появлялась ровно из автомата
        self.speed = speed  # флаг в какую сторону полетит пуля

    def update(self, *args, **kwargs) -> None:
        # уничтожение пули если она столкнулась со стеной или с гоблином
        if pygame.sprite.spritecollideany(self, blocks_wall) or pygame.sprite.spritecollideany(self, mob_group):
            self.kill()

        # координаты движения пули
        SPEED_BULLET = 20  # скорость пули
        if self.speed is True:
            self.rect.x += SPEED_BULLET
        else:
            self.rect.x -= SPEED_BULLET


class Automaton(pygame.sprite.Sprite):
    """Автомат
    """

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1] + 16  # чтобы автомат был в руках у персонажа

        self.count = 0
        self.count_plus = -1

    def update(self, *args, **kwargs) -> None:
        cord = player.rect  # координаты игрока
        cord_x = cord[0]
        cord_y = cord[1]

        self.rect.x = cord_x
        self.rect.y = cord_y + 16  # чтобы пуля спавнилась в автомате

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # спавн пуль при нажатий на пробел
            if self.count % 10 == 0:
                if player.right_or_left == "./data/automaton.png":
                    # спавн пули летящей вправо
                    Bullet("./data/pul_right.png", (self.rect.x, self.rect.y - size), True, size, bullet_group, all)
                else:
                    # спавн пули летящей влево
                    Bullet("./data/pul_left.png", (self.rect.x, self.rect.y - size), False, size, bullet_group, all)
                self.count_plus *= -1
            self.count += self.count_plus


class NpcOne(pygame.sprite.Sprite):
    """NPC
    Дает квест
    Вывод текст на вверх экрана"""

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.flag_kvest = False  # флаг на выдан ли уже квест
        self.count = 0  # число убитых гоблинов

        self.font = pygame.font.SysFont('Comic Sans MS', 10)  # шрифт
        self.text = ""  # текст вывода

    def update(self, *args, **kwargs) -> None:
        # если персонаж коснулся NPC
        if pygame.sprite.spritecollideany(self, player_group):
            # пополняется здоровье, если персонаж убил 5 гоблинов и до этого подошел к нему за квестом
            UP_HP = 20  # востоновление здоровья
            FULL_HP = 100  # полное здоровье
            if self.flag_kvest is True and self.count >= 5:
                if player.hp_player + UP_HP <= FULL_HP:
                    player.hp_player += UP_HP
                elif player.hp_player + UP_HP > FULL_HP:
                    player.hp_player = FULL_HP
                # сброс настроек
                self.flag_kvest = False
                self.count = 0
                self.text = ""
            else:
                # персонаж подошел за квестом
                self.text = "Убей 5 гоблинов, и приходи ко мне!"
                self.count = 0
                self.flag_kvest = True

        # отображение слво NPC
        text_start = self.font.render(self.text, False, (0, 0, 0))
        display.blit(text_start, (150, 20))


class Box(pygame.sprite.Sprite):
    """Сундук
    Смена спрайта
    Восполнение здоровья персонажа"""

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.sound_open_box = pygame.mixer.Sound("./data/sound/music_box.mp3")  # музыка открывания сундука

        self.flag_open = True  # флаг для того чтобы открыть сундук только один раз

    def update(self, *args, **kwargs) -> None:
        # если персонаж коснулся сундука и до этого не касался
        if pygame.sprite.spritecollideany(self, player_group) and self.flag_open:
            self.flag_open = False  # флаг, то что уже открыл
            self.image = pygame.image.load("./data/open_box.png")
            # востановление здоровья
            UP_HP = 20  # востоновление здоровья
            FULL_HP = 100  # полное здоровье
            if player.hp_player + UP_HP <= FULL_HP:
                player.hp_player += UP_HP
            elif player.hp_player + UP_HP > FULL_HP:
                player.hp_player = FULL_HP
            self.sound_open_box.play()


class MobSpawner(pygame.sprite.Sprite):
    """Спавнер гоблинов"""

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.timer_spawner = 0
        self.time_plus = -1

    def update(self, *args, **kwargs) -> None:
        # если спавнеры находядтся на растояний не больше 400 пикслей
        CORD_MIN_SPAWN = 0  # минимальное расстояние от героя когда могут спавниться мобы
        CORD_MAX_SPAWN = 400  # максимальное расстоние от героя когда могут спавниться мобы
        TIME_SPAWN_GOBLIN = [200, 0]  # время появления гоблинов
        if (CORD_MIN_SPAWN < abs(player.rect.x - self.rect.x) < CORD_MAX_SPAWN) and \
                (CORD_MIN_SPAWN < abs(player.rect.y - self.rect.y) < CORD_MAX_SPAWN):
            if self.timer_spawner in TIME_SPAWN_GOBLIN:
                self.time_plus *= -1
                # спавнится гоблин
                Mob("./data/goblin/idle_start.png", (self.rect.x, self.rect.y), size, mob_group, all)
            self.timer_spawner += self.time_plus


class Mob(pygame.sprite.Sprite):
    """гоблин
    наносит урон персонажу
    двигается навстречу персонажу
    умирает"""

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.count = -1
        self.count_image = 0
        # спрайты движения гоблина вправо
        self.image_run_right = [pygame.image.load("./data/goblin/run_right/Run_1.png"),
                                pygame.image.load("./data/goblin/run_right/Run_2.png"),
                                pygame.image.load("./data/goblin/run_right/Run_3.png"),
                                pygame.image.load("./data/goblin/run_right/Run_4.png")]

        # спрайты движения гоблина влево
        self.image_run_left = [pygame.image.load("./data/goblin/run_left/m_Run_1.png"),
                               pygame.image.load("./data/goblin/run_left/m_Run_2.png"),
                               pygame.image.load("./data/goblin/run_left/m_Run_3.png"),
                               pygame.image.load("./data/goblin/run_left/m_Run_4.png")]

        self.hp_goblin = 100  # жизни гоблина

    def update(self, *args, **kwargs) -> None:
        old_player_pos = self.rect.x, self.rect.y

        cord_player = player.cord()  # кординаты персонажа
        cord_player_x = cord_player[0]
        cord_player_y = cord_player[1]

        # если гоблин касается персонажа то наносит ему урон
        DAMAGE_GOBLIN = 1
        if pygame.sprite.spritecollideany(self, player_group):
            player.hp_player -= DAMAGE_GOBLIN  # урон 1

        # если пули попадают в гоблина то у гоблина отнимаются жизни
        DAMAGE_HEROES = 25
        if pygame.sprite.spritecollideany(self, bullet_group):
            self.hp_goblin -= DAMAGE_HEROES  # урон по гоблину 25
            # если у гоблина меньше 0 жизней он умирает
            if self.hp_goblin <= 0:
                if npc.flag_kvest is True:
                    npc.count += 1
                self.kill()

        # движние гоблина
        STEP = 2
        if cord_player_x < self.rect.x:
            self.rect.x -= STEP
            self.image = self.image_run_left[self.count_image // 10]
        if cord_player_x > self.rect.x:
            self.rect.x += STEP
            self.image = self.image_run_right[self.count_image // 10]
        if cord_player_y < self.rect.y:
            self.rect.y -= STEP
        if cord_player_y > self.rect.y:
            self.rect.y += STEP

        # если гоблин касается стены то останавливется
        if pygame.sprite.spritecollideany(self, blocks_wall):
            self.rect.x, self.rect.y = old_player_pos
            return

        if self.count_image % 39 == 0:
            self.count *= -1
        self.count_image += self.count


class Finish(pygame.sprite.Sprite):
    """блок Финиша
    если персонаж его касается то появляется окно финиша"""

    def __init__(self, color, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def finish_screen(self):
        # музыка выигрыша
        sound_happy = pygame.mixer.Sound("./data/sound/music_happy.mp3")
        sound_happy.set_volume(0.05)
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # картинка выигрыша
            start_fon = pygame.image.load("./data/finish_game.jpg")
            display.blit(start_fon, (0, 0))

            # текст выигрыша
            font = pygame.font.SysFont('Comic Sans MS', 27)
            text = """УРААА!!! ВЫ ПРОШЛИ ИГРУ!!!"""
            text_start = font.render(text, False, (10, 70, 166))
            display.blit(text_start, (7, 0))

            sound_happy.play()

            pygame.display.flip()

    def update(self, *args, **kwargs) -> None:
        # если персонаж касается
        if pygame.sprite.spritecollideany(self, player_group):
            self.finish_screen()


class Wall(pygame.sprite.Sprite):
    """блок стены
    в этом классе ничего не делает(кроме того как ставит на себя спарйт)
    а так в  других классах ограничевает выход за карту"""

    def __init__(self, name, pos, size: int, *groups: AbstractGroup):
        super().__init__(*groups)

        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load(name)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def start_screen():
    """стартовое окно"""
    flag = True

    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # если нажать по этим кооржинатам(где находится кнопка) то игра начнется
        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        pos_x, pos_y = pos[0], pos[1]
        if pressed[0] is True and (100 <= pos_x <= 300) and (50 <= pos_y <= 100):
            flag = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            flag = False

        # фоновое изображение
        start_fon = pygame.image.load("./data/start_fon.jpg")
        display.blit(start_fon, (0, 0))

        pygame.draw.rect(display, (71, 71, 71), (100, 50, 200, 50))

        # кнопка, ддя начала игры
        font = pygame.font.SysFont('Comic Sans MS', 30)
        text_start = font.render('начать', False, (0, 0, 0))
        display.blit(text_start, (160, 50))

        pygame.display.flip()


def game_over():
    """окно проигрыша"""
    # музыка для проигрыша
    sound_game_over = pygame.mixer.Sound("./data/sound/music_gameover.mp3")
    sound_game_over.set_volume(0.02)  # громкость звука
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        # скример
        start_fon = pygame.image.load("./data/game_over.jpg")
        display.blit(start_fon, (0, 0))
        sound_game_over.play()

        pygame.display.flip()


if __name__ in "__main__":
    window = (400, 400)
    FPS = 60
    display = pygame.display.set_mode(window)
    clock = pygame.time.Clock()
    sound_game = pygame.mixer.Sound("./data/sound/music_prosto.mp3")
    sound_game.set_volume(0.02)  # громкость звука
    size = 16  # размер блока

    world = pygame.Surface((2000, 2000))
    all = pygame.sprite.Group()  # все объекты
    blocks_wall = pygame.sprite.Group()  # стены
    blocks_box = pygame.sprite.Group()  # сундуки
    player_group = pygame.sprite.GroupSingle()  # персонаж
    npc_group = pygame.sprite.Group()  # NPC
    mob_group = pygame.sprite.Group()  # гоблины
    bullet_group = pygame.sprite.Group()  # пули
    finish_group = pygame.sprite.Group()  # блок финиш

    camera = Camera((150, 150))  # координаты камеры
    player = Player(camera, all, player_group)
    automaton = Automaton("./data/automaton.png", (32, 32), size, all)  # автомат

    with open('first_level.txt', 'r') as first_level:
        x = y = 0  # координаты
        for y, row in enumerate(first_level):  # вся строка
            for x, col in enumerate(row):  # каждый символ
                if col == ".":  # спавн стен
                    Wall("./data/wall.png", (x * size, y * size), size, blocks_wall, all)
                elif col == "B":  # спавн сундуков
                    Box("./data/box.png", (x * size, y * size), size, blocks_box, all)
                elif col == "N":  # NPC
                    npc = NpcOne("./data/npc_one.png", (x * size, y * size), size, npc_group, all)
                elif col == "M":  # спавн спавнеров гоблинов
                    MobSpawner("./data/spawner.png", (x * size, y * size), size, mob_group, all)
                elif col == "F":  # спавн блока финиша
                    Finish(colors["YELLOW"], (x * size, y * size), size, finish_group, all)

    start_screen()  # стартовое окно, пока оно не закроется игра не начнется
    sound_game.play()  # звук игры
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if player.hp_player <= 0:  # если у игрока 0 жизней игра заканчиается
            game_over()

        display.fill(colors["GREY"])
        world.fill(colors["BROWN"])
        all.draw(world)
        display.blit(world, camera.pos)

        all.update()
        pygame.display.flip()
