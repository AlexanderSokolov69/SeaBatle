from random import randint

import pygame.sprite

from modules.ingame import *
from modules.sql_games import *


class Cursor(pygame.sprite.Sprite):
    """
    Класс, реализующий различные курсоры с анимацией
    """
    ANIM_FREEZE = 1

    def __init__(self, fname, columns, rows):
        super(Cursor, self).__init__(cursor_sprites)
        self.frames = []
        self.frame = 0
        self.cut_images(load_image(fname), columns, rows)
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect()
        self.next_pos = 0, 0
        self.time = 0
        self.freeze = Cursor.ANIM_FREEZE

    def cut_images(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self, pos, time):
        self.next_pos = pos
        self.time = time

    def shot(self):
        self.frame = 1

    def update(self):
        self.image = self.frames[self.frame]
        if self.frame:
            if self.freeze <= 0:
                self.frame = (self.frame + 1) % len(self.frames)
                self.freeze = Cursor.ANIM_FREEZE
            else:
                self.freeze -= 1
        if self.time <= 0:
            self.rect.x = self.next_pos[0]
            self.rect.y = self.next_pos[1]
        else:
            frames = FPS * (self.time / 1000)
            dx = (self.next_pos[0] - self.rect.x) / frames
            dy = (self.next_pos[1] - self.rect.y) / frames
            self.rect.x += 5 * dx
            self.rect.y += 5 * dy
            self.time -= self.time // frames


class Button(pygame.sprite.Sprite):
    """
    Реализация кнопок меню, участвуют в "пасхальной" последовательности
    """
    def __init__(self, x, y, text, uid=0):
        super(Button, self).__init__(game_sprites)
        self.image2 = image_convert(load_image('menu2.PNG'))
        self.image1 = image_convert(load_image('menu.PNG'))
        font = pygame.font.Font(None, 60)
        text = font.render(text, True, 'brown')
        self.image1.blit(text, (32, 35))
        self.image2.blit(text, (32 + 5, 35 + 5))
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.uid = uid
        self.count = 0

    def check_click(self, mouse):
        if ret := self.rect.collidepoint(mouse):
            self.count = FPS // 4
        return ret

    def update(self):
        if self.count > 0:
            self.image = self.image2
            self.count -= 1
        else:
            self.image = self.image1


class Boat(pygame.sprite.Sprite):
    """
    Анимированные корабли противников, участвуют в "пасхальной" последовательности
    """
    def __init__(self, x, y, fimage, uid=0):
        super(Boat, self).__init__(game_sprites)
        self.image = pygame.transform.scale(load_image(fimage), (140, 140))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.fps = FPS
        self.uid = uid
        self.count = 0

    def update(self):
        if self.count > 0:
            self.count -= 1
            self.rect.x = self.x + randint(-2, 2)
            self.rect.y = self.y + randint(-2, 2)
        else:
            self.fps -= 3
            if self.fps <= 0:
                self.fps = FPS
                self.rect.x = self.x + randint(-4, 4)
                self.rect.y = self.y + randint(-2, 2)

    def check_click(self, mouse):
        if ret := self.rect.collidepoint(mouse):
            self.count = FPS
        return ret


class SplashShot(pygame.sprite.Sprite):
    """
    Летающее ядро на заставке
    """
    def __init__(self, x, y):
        super(SplashShot, self).__init__(splash_sprites)
        self.image = load_image('shot02.PNG')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.dx = randint(10, 30)
        self.dy = randint(-18, -10)
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
    """
    Анимированные корабли на заставке
    """
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
            self.rect.x = self.x + randint(-10, 10)
            self.rect.y = self.y + randint(-4, 4)
