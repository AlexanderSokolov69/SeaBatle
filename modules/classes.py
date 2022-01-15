import random
import pygame

from modules.const import *
from modules.sql_games import DBase, Table, play_sound, load_music, load_image, image_convert


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super(Cursor, self).__init__(cursor_sprites)
        self.image = load_image('cursor.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super(Button, self).__init__(game_sprites)
        self.image = image_convert(load_image('menu.PNG'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        font = pygame.font.Font(None, 60)
        text = font.render(text, True, 'brown')
        self.image.blit(text, (32, 35))

    def check_click(self, mouse):
        return self.rect.collidepoint(mouse)


class Boat(pygame.sprite.Sprite):
    def __init__(self, x, y, fimage):
        super(Boat, self).__init__(game_sprites)
        self.image = pygame.transform.scale(load_image(fimage), (140, 140))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.fps = FPS

    def update(self):
        self.fps -= 3
        if self.fps <= 0:
            self.fps = FPS
            self.rect.x = self.x + random.randint(-4, 4)
            self.rect.y = self.y + random.randint(-2, 2)


class SplashShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(SplashShot, self).__init__(splash_sprites)
        self.image = load_image('shot02.PNG')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = random.randint(10, 20)
        self.dy = random.randint(-18, -10)
        self.grav = 1
        play_sound('explore01.ogg')

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dy += self.grav
        if not self.rect.colliderect(screen_rect):
            play_sound('explore00.ogg')
            self.kill()


class SplashBoat(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super(SplashBoat, self).__init__(splash_sprites)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.fps = FPS0
        
    def update(self):
        self.fps -= 3
        if self.fps <= 0:
            self.fps = FPS0
            self.rect.x = self.x + random.randint(-10, 10)
            self.rect.y = self.y + random.randint(-4, 4)
