import os
import random
import sys
import pygame
from modules.base import Sea
from modules.ai import AI
from modules.sql_games import DBase, Table, play_sound, load_music

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()

pygame.display.set_caption('Морской бой')
pygame.mixer.music.set_volume(0.3)
load_music("music.mp3")
clock = pygame.time.Clock()
fps = 40
DOP_SHOT = 3000
size = width, height = 1250, 700
db = DBase(os.path.join('modules', 'seabase.db'))
splash_sprites = pygame.sprite.Group()
game_sprites = pygame.sprite.Group()
screen_rect = pygame.Rect((0, 0), (width, height))
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


def image_convert(image, color_key=None):
    if not color_key:
        color_key = image.get_at((0, 0))
    image.set_colorkey(color_key)
    return image.convert_alpha()


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        super(Button, self).__init__(game_sprites)
        self.image = image_convert(Table('img').get_image('menu.PNG')['menu.PNG'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        font = pygame.font.Font(None, 60)
        text = font.render(text, True, 'brown')
        self.image.blit(text, (30, 30))
    
    def check_click(self, mouse):
        return self.rect.collidepoint(mouse)


class Boat(pygame.sprite.Sprite):
    def __init__(self, x, y, fimage):
        super(Boat, self).__init__(game_sprites)
        self.image = pygame.transform.scale(image_convert(Table('img').get_image(fimage)[fimage]), (140, 140))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Splash_Shot(pygame.sprite.Sprite):
    image = image_convert(Table('img').get_image('shot02.PNG')['shot02.PNG'].convert_alpha())

    def __init__(self, x, y):
        super(Splash_Shot, self).__init__(splash_sprites)
        self.image = Splash_Shot.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 50
        self.dy = -40
        self.grav = 5
        play_sound('explore01.ogg')

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dy += self.grav
        if not self.rect.colliderect(screen_rect):
            play_sound('explore00.ogg')
            self.kill()


# ---------------------------------------------------------------------------
def terminate():
    """ Завершение игры """
    pygame.quit()
    sys.exit()


def show_stat(screen):
    """
    Формирование дополнительной графики, вне игровых полей
    :param screen:
    :return:
    """
    font = pygame.font.Font(None, 60)
    text = font.render("МОРСКОЙ БОЙ", True, 'red')
    screen.blit(text, (400, 10))
    font = pygame.font.Font(None, 30)
    text = font.render("(SPACE - new game, M - music on/off)", True, 'brown')
    screen.blit(text, (380, 55))


def AI_move(board):
    """
    Выполнение хода компьютером
    :param board:
    :return:
    """
    if board.score() > 0:
        if board.last_shot:
            cnt = 0
            coords = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (0, 2), (0, -2), (2, 0), (-2, 0)]
            x, y = board.last_coord
            while board.board[x][y] in {1, 11, 12}:
                x = max(min(board.last_coord[0] + coords[cnt][0], 9), 0)
                y = max(min(board.last_coord[1] + coords[cnt][1], 9), 0)
                cnt += 1
                if cnt > 7:
                    board.last_shot = False
                    break
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            while board.board[x][y] in {1, 11, 12}:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
        board.on_click((x, y))


def change_music(state):
    """
    Включение / выключение музыкального трека
    :param state:
    :return:
    """
    if state:
        pygame.mixer.music.play(-1)
        return False
    else:
        pygame.mixer.music.stop()
        return True

def win_screen(screen, scr01, scr02, move01, move02):
    if scr02 == 0:
        outline = f"ПОБЕДА!"
        color = 'green'
        fsize = 60
    elif scr01 == 0:
        outline = f"НЕ ПОВЕЗЛО!"
        color = 'red'
        fsize = 60
    elif scr01 > scr02:
        outline = f"Так держать!"
        color = 'blue'
        fsize = 40
    else:
        outline = f"Соберись!"
        color = 'magenta'
        fsize = 40
    font = pygame.font.Font(None, fsize)
    text = font.render(outline, True, color)
    screen.blit(text, (100, height - 80))
    outline = f"счёт  {scr01} : {scr02}"
    font = pygame.font.Font(None, fsize)
    text = font.render(outline, True, color)
    screen.blit(text, (fsize * 8, height - 80))
    outline = f"ходы  ты: {move02}  робот: {move01}"
    font = pygame.font.Font(None, 30)
    text = font.render(outline, True, 'black')
    screen.blit(text, (100, height - 30))

if __name__ == '__main__':
    music_state = change_music(True)
    running = True
    # -----SPLASH START----------------------------
    pygame.time.set_timer(pygame.USEREVENT + 1, 3500)
    text_info = [' Сыграй с жуликом и победи!',
                 'Противник делает ход каждые',
                 '   3 секунды вне очереди',
                 ' и каждый раз после тебя...',
                 '',
                 '',
                 '         PRESS ANY KEY']
    pygame.key.set_repeat(200, 60)
    # font = pygame.font.Font(None, 30)
    # step = 50
    # dx = 50
    # for i in range(len(title)):
    #     string = font.render(title[i], True, 'white')
    #     screen.blit(string, (dx, step * (i + 1)))
    img0 = image_convert(Table('img').get_image('title.png')['title.png'].convert_alpha())
    img1 = image_convert(Table('img').get_image('ship02.PNG')['ship02.PNG'])
    img2 = image_convert(Table('img').get_image('ship01.png')['ship01.png'])
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                cont = False
            if event.type == (pygame.USEREVENT + 1):
                Splash_Shot(150, 500)
        screen.fill('blue')
        font = pygame.font.Font(None, 50)
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        screen.blit(img2, (850 + dx, 400 + dy))
        splash_sprites.draw(screen)
        splash_sprites.update()
        step = 50
        dx = 400
        for i in range(len(text_info)):
            string = font.render(text_info[i], True, 'white')
            screen.blit(string, (dx, step * i + 300))
        screen.blit(img0, (250, 20))
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        screen.blit(img1, (100 + dx, 400 + dy))
        pygame.display.flip()
        clock.tick(6)

    # ----- SPLASH END ----------------------------
    pygame.time.set_timer(pygame.USEREVENT, DOP_SHOT)
    load_music("battle.ogg")
    music_state = change_music(True)
    field1 = Sea(0)
    field1.fill(AI().get_coords())
    field2 = Sea(1)
    field2.fill(AI().get_coords())
    gaming = True
    gr = 240
    step = 1
    spr01 = Button(width - 270, 50, 'ЗАНОВО')
    spr02 = Button(width - 270, 200, 'МУЗЫКА')
    spr03 = Button(width - 270, 350, ' ВЫХОД')
    Boat(10, 10, 'ship02.PNG')
    Boat(900, height - 150, 'ship01.png')
    darkout = True
    while darkout or running:
        if gaming:
            gr = 240
            darkout = True
        else:
            if gr >= 240:
                step = -2
            if gr < 100:
                step = 0
                darkout = False
            gr += step
        screen.fill((gr, gr, gr))
        win_screen(screen, field1.score(), field2.score(), field1.move, field2.move)
        # if not gaming:
        #     win_screen(screen, field1.score(), field2.score())
        show_stat(screen)
        if (field1.score() == 0 or field2.score() == 0) and gaming == True:
            gaming = False
            load_music("music.mp3")
            music_state = change_music(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gaming = False
            if event.type in (pygame.USEREVENT, pygame.USEREVENT + 2):
                if gaming:
                    pygame.time.set_timer(pygame.USEREVENT, DOP_SHOT)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                    AI_move(field1)  # Основной и Дополнительный ход компьютера
                    field2.resetflag()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if spr01.check_click(event.pos):
                        load_music("battle.ogg")
                        music_state = change_music(True)
                        field1.fill(AI().get_coords())
                        field2.fill(AI().get_coords())
                        gaming = True
                    elif spr02.check_click(event.pos):
                        music_state = change_music(music_state)
                    elif spr03.check_click(event.pos):
                        running = False
                        gaming = False
                    elif gaming:
                        if not field2.getflag() and field2.get_click(event.pos):
                            pygame.time.set_timer(pygame.USEREVENT, 0)
                            pygame.time.set_timer(pygame.USEREVENT + 2, 500)
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEMOTION:
                vx, vy = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_state = change_music(music_state)
                if event.key == pygame.K_SPACE:
                    load_music("battle.ogg")
                    music_state = change_music(True)
                    field1.fill(AI().get_coords())
                    field2.fill(AI().get_coords())
                    gaming = True

        field1.render(screen)
        field2.render(screen)
        game_sprites.draw(screen)
        game_sprites.update()
        
        clock.tick(fps)
        pygame.display.flip()
    terminate()

