import pygame

from modules.ingame import *

FPS0 = 30   # FPS начального экрана
FPS = 60    # FPS игрового интерфейса
TIMER_SPLASH = 3500  # Периодичность анимации стартового экрана
size = width, height = 1250, 700  # Размер игрового поля
screen_rect = pygame.Rect((0, 0), (width, height))  # Зона существования спрайтов
GR_HIGH = 220  # Максимальная яркость фона игрового поля
BR_STEP = 2  # Шаг изменения яркости фона
FOG_OFF = [1, 2, 3, 4]  # "Пасхальная" последовательность. (отключает "туман войны")
TIME_AI_MOVE = 500  # Продолжительность анимации хода компьютера

splash_sprites = pygame.sprite.Group()  # Спрайты начального экрана
game_sprites = pygame.sprite.Group()  # Спрайты игры нижнего слоя
cursor_sprites = pygame.sprite.Group()  # Спрайты игры верхнего слоя


class P:
    """
    Настраиваемые через settings.ini параметры игры
    """
    DB_NAME = 'seabase.db'  # Место и имя БД с изображениями и логом игр
    PATH_M = 'modules/snd'  # Папка со сзвуками и музыкой
    DOP_SHOT = 3000  # Период стрельбы без очереди ms. 0 - отключение
    M_VOLUME = 0.4  # Громкость музыкального сопровождения
    music_0 = 'music.mp3'  # Музыка на заставку и проигрыш игрока
    music_1 = 'battle.mp3'  # Музыка боя
    music_2 = 'winners.mp3'  # Выигрыш игрока
    GR_LOW = 100  # Минимальная яркость фона игрового поля
    WIN_STAT = 'window'  # Режим работы игры "fullscreen" и "window"

    @classmethod
    def config_parse(cls, conf):
        try:
            cls.DB_NAME = conf['Struct']['dbpath']
        except Exception:
            pass
        try:
            cls.PATH_M = conf['Struct']['sndpath']
        except Exception:
            pass
        try:
            cls.DOP_SHOT = int(conf['Timing']['dop_shot']) * 1000
        except Exception:
            pass
        try:
            cls.M_VOLUME = float(conf['Music']['volume'])
        except Exception:
            pass
        try:
            cls.music_0 = conf['Music']['music_splash']
        except Exception:
            pass
        try:
            cls.music_1 = conf['Music']['music_battle']
        except Exception:
            pass
        try:
            cls.music_2 = conf['Music']['music_winner']
        except Exception:
            pass
        try:
            cls.GR_LOW = int(conf['Interface']['low_bright'])
        except Exception:
            pass
        try:
            cls.WIN_STAT = conf['Interface']['screen']
        except Exception:
            pass
