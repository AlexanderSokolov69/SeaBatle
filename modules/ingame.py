import random
import sys

from modules.const import *


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


def ai_move(board):
    """
    Выполнение хода компьютером
    :param board:
    :return:
    """
    if board.score() > 0:
        if board.last_shot:
            cnt = 0
            coords = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            x, y = board.last_coord
            while board.board[x][y] in {1, 11, 12}:
                shift = random.choice(coords)
                x = max(min(board.last_coord[0] + shift[0], 9), 0)
                y = max(min(board.last_coord[1] + shift[1], 9), 0)
                cnt += 1
                if cnt > 12:
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
