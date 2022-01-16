from random import randint, choice

from modules.ingame import *

"""
Класс AI, формирующий при создании множество координат кораблей, случайным образом 
размещенных на игровом поле.
"""


class AI:
    def __init__(self):
        self.graph = {  # Базовые наборы координат кораблей и зон отчуждения вокруг них
            '4-1': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1), (3, -1, 1), (4, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1), (3, 1, 1), (4, 1, 1)],
            '3-1': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1), (3, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1), (3, 1, 1)],
            '3-2': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1), (3, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1), (3, 1, 1)],
            '2-1': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1)],
            '2-2': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1)],
            '2-3': [(-1, 0, 1), (0, 0, 0), (1, 0, 0), (2, 0, 1),
                    (-1, -1, 1), (0, -1, 1), (1, -1, 1), (2, -1, 1),
                    (-1, 1, 1), (0, 1, 1), (1, 1, 1), (2, 1, 1)],
            '1-1': [(0, 0, 0), (-1, 0, 1), (1, 0, 1), (-1, -1, 1),
                    (0, -1, 1), (1, -1, 1), (-1, 1, 1),
                    (0, 1, 1), (1, 1, 1)],
            '1-2': [(0, 0, 0), (-1, 0, 1), (1, 0, 1), (-1, -1, 1),
                    (0, -1, 1), (1, -1, 1), (-1, 1, 1),
                    (0, 1, 1), (1, 1, 1)],
            '1-3': [(0, 0, 0), (-1, 0, 1), (1, 0, 1), (-1, -1, 1),
                    (0, -1, 1), (1, -1, 1), (-1, 1, 1),
                    (0, 1, 1), (1, 1, 1)],
            '1-4': [(0, 0, 0), (-1, 0, 1), (1, 0, 1), (-1, -1, 1),
                    (0, -1, 1), (1, -1, 1), (-1, 1, 1),
                    (0, 1, 1), (1, 1, 1)],
        }
        self.list = set()
        for ship in self.graph:
            count = 10000
            # Если за COUNT попыток не удалось разместить очередной корабль
            # на игровом поле - попытки прекращаются
            while self.chk(self.graph[ship], choice([False, True]),
                           randint(0, 10 - int(ship[0])),
                           randint(0, 10 - int(ship[0]))):
                count -= 1
                if count == 0:
                    break

    def chk(self, coords, swap, x, y):
        """
        Функция проверяет на корректность размещение корабля на поле.
        :param coords: список координат корабля
        :param swap: направление размещения вертикально/горизонтально
        :param x:
        :param y:
        :return: True - возможно. False - не влезает
        """
        for coord in coords:
            dx = coord[0] + x
            dy = coord[1] + y
            if swap:
                dx, dy = dy, dx
            if (dx, dy) in self.list:
                return True
        for coord in coords:
            if coord[2] == 0:
                dx = coord[0] + x
                dy = coord[1] + y
                self.list.add((dy, dx) if swap else (dx, dy))
        return False

    def get_coords(self):
        """
        Возвращает множество координат кораблей
        :return:
        """
        return self.list
