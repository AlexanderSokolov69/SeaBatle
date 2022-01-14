import pygame

FPS0 = 15
FPS = 40
TIMER_SPLASH = 3500
size = width, height = 1250, 700
screen_rect = pygame.Rect((0, 0), (width, height))
GR_HIGH = 240
BR_STEP = 2

splash_sprites = pygame.sprite.Group()
game_sprites = pygame.sprite.Group()


class P:
    DB_NAME = 'modules/seabase.db'
    PATH_M = 'modules/snd'
    DOP_SHOT = 3000
    M_VOLUME = 0.4
    music_0 = 'music.mp3'
    music_1 = 'battle.ogg'
    GR_LOW = 100
    WIN_STAT = 'window'

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
            cls.GR_LOW = int(conf['Interface']['low_bright'])
        except Exception:
            pass
        try:
            cls.WIN_STAT = conf['Interface']['screen']
        except Exception:
            pass
