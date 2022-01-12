import random
import sys
import pygame
from modules.base import Sea
from modules.ai import AI
from modules.sql_games import DBase, Table

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
pygame.init()

pygame.display.set_caption('Морской бой')
pygame.mixer.music.load("music.mp3")
clock = pygame.time.Clock()
fps = 30
pygame.mixer.music.set_volume(0.5)
size = width, height = 1200, 700
db = DBase('seabase.db')
splash_sprites = pygame.sprite.Group()
screen_rect = pygame.Rect((0, 0), (width, height))
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


def image_convert(image, color_key=None):
    if not color_key:
        color_key = image.get_at((0, 0))
    image.set_colorkey(color_key)
    return image.convert_alpha()


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

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.dy += self.grav
        if not self.rect.colliderect(screen_rect):
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
    text = font.render("Sea Battle", True, 'red')
    screen.blit(text, (400, 5))
    font = pygame.font.Font(None, 30)
    text = font.render("(SPACE - new game, M - music on/off)", True, 'brown')
    screen.blit(text, (300, 50))


def AI_move(board):
    """
    Выполнение хода компьютером
    :param board:
    :return:
    """
    if board.score() > 0:
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
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    field1 = Sea(0)
    field1.fill(AI().get_coords())
    field2 = Sea(1)
    field2.fill(AI().get_coords())
    gaming = True
    gr = 240
    step = 1
    while running:
        if gaming:
            gr = 240
        else:
            if gr > 240:
                step = -1
            if gr < 200:
                step = 1
            gr += step
        screen.fill((240, gr, gr))
        show_stat(screen)
        if (field1.score() == 0 or field2.score() == 0) and gaming == True:
            gaming = False
            music_state = change_music(True)
            pygame.mixer.Sound('expl\explore03.ogg').play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if gaming:
                    AI_move(field1)  # Дополнительный ход компьютера
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if gaming:
                        field2.get_click(event.pos)
                        if field2.getflag():
                            AI_move(field1)
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.MOUSEMOTION:
                vx, vy = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_state = change_music(music_state)
                if event.key == pygame.K_SPACE:
                    field1.fill(AI().get_coords())
                    field2.fill(AI().get_coords())
                    gaming = True

        field1.render(screen)
        field2.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    terminate()

