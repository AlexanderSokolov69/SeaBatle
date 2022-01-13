import pygame

FPS0 = 6
FPS = 40
DOP_SHOT = 3000
TIMER_SPLASH = 3500
size = width, height = 1250, 700
screen_rect = pygame.Rect((0, 0), (width, height))
GR_HIGH = 240
GR_LOW = 100
BR_STEP = 1

M_VOLUME = 0.4

DB_NAME = 'modules/seabase.db'
PATH_M = 'modules/snd'
music_0 = "music.mp3"
music_1 = "battle.ogg"
splash_sprites = pygame.sprite.Group()
game_sprites = pygame.sprite.Group()
