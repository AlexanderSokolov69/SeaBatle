from os import path
from sys import exit
from random import randint, choice

from modules.const import *
from modules.sql_games import Table


def terminate():
    """ Завершение игры """
    pygame.quit()
    exit()


def show_stat(screen, text_low):
    """
    Формирование дополнительной графики, вне игровых полей
    """
    font = pygame.font.Font(None, 60)
    text = font.render("МОРСКОЙ БОЙ", True, 'black')
    screen.blit(text, (403, 13))
    text = font.render("МОРСКОЙ БОЙ", True, 'red')
    screen.blit(text, (400, 10))
    font = pygame.font.Font(None, 30)
    text = font.render(text_low, True, 'brown')
    screen.blit(text, (360, 55))


def ai_move(board):
    """
    Выполнение хода компьютером
    По последним двум попаданиям пытается выяснить направление расположения корабля противника
    и выполнить выстрел по соседним полям.
    Если это не удаётся, выстрел выполняется в случайное свободное поле.
    """
    if board.score() > 0:
        if board.last_shot:
            cnt = 0
            coords = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if len(board.move_queue) > 1:
                dx = abs(board.move_queue[-1][0] - board.move_queue[-2][0])
                dy = abs(board.move_queue[-1][1] - board.move_queue[-2][1])
                if dx + dy == 1:
                    if dx == 0:
                        coords = [(0, 1), (0, -1), (0, 2), (0, -2)]
                    else:
                        coords = [(1, 0), (-1, 0), (2, 0), (-2, 0)]
            x, y = board.move_queue[-1]
            sx, sy = board.move_queue[-1]
            while board.board[x][y] in {1, 11, 12}:
                shift = choice(coords)
                x = max(min(sx + shift[0], 9), 0)
                y = max(min(sy + shift[1], 9), 0)
                cnt += 1
                if cnt > 20:
                    board.last_shot = False
                    break
        else:
            x = randint(0, 9)
            y = randint(0, 9)
            while board.board[x][y] in {1, 11, 12}:
                x = randint(0, 9)
                y = randint(0, 9)
        board.next_move = x, y
        # board.on_click((x, y))
        return board.left + board.cell_size * x, board.top + board.cell_size * y


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
    """
    Формирование информационных и мотивирующих игровых строк внизу экрана
    """
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
        color = 'firebrick1'
        fsize = 40
    font = pygame.font.Font(None, fsize)
    text = font.render(outline, True, color)
    screen.blit(text, (100, height - 80))
    outline = f"счёт  {scr01} : {scr02}"
    font = pygame.font.Font(None, fsize)
    text = font.render(outline, True, color)
    screen.blit(text, (fsize * 8, height - 80))
    outline = f"ходы  игрок: {move02}  робот: {move01}"
    font = pygame.font.Font(None, 30)
    text = font.render(outline, True, 'blue')
    screen.blit(text, (100, height - 30))
    font = pygame.font.Font(None, 20)
    i = 0
    log = list(Table('log').get().values())
    for values in log[-1: -16: -1]:
        text = f"счёт ({values['sc01']}:{values['sc02']}). ходы ({values['move02']}:{values['move01']})"
        color = 'darkgreen' if values['sc01'] > values['sc02'] else 'darkred'
        string = font.render(text, True, color)
        screen.blit(string, (width - 190, 20 * i + height - 330))
        i += 1


def play_sound(name):
    """
    Загрузка в свободный канал миксера звукового эффекта
    """
    if ch := pygame.mixer.find_channel(True):
        file = path.join(P.PATH_M, name)
        ch.play(pygame.mixer.Sound(file))


def load_music(name, volume):
    """
    Загрузка музыкального трека
    """
    file = path.join(P.PATH_M, name)
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(volume)
