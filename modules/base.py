from modules.sql_games import *
from modules.ingame import *

class Field(pygame.sprite.Sprite):
    def __init__(self, x, y, fsize):
        super(Field, self).__init__(game_sprites)
        self.image = pygame.transform.scale(load_image('field.png'), fsize)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Board:
    """
    Базовый класс Board
    """
    # создание поля
    def __init__(self, wx, hy):
        self.width = wx
        self.height = hy
        self.board = [[0] * hy for _ in range(wx)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.boardcolor = 'black'
        self.flag = False

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        Field(left, top, (cell_size * self.width, cell_size * self.height))

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(screen, self.boardcolor,
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

    def get_cell(self, mouse_pos):
        if self.left < mouse_pos[0] < self.left + self.cell_size * self.width \
                and self.top < mouse_pos[1] < self.top + self.cell_size * self.height:
            return ((mouse_pos[0] - self.left) // self.cell_size,
                    (mouse_pos[1] - self.top) // self.cell_size)

    def on_click(self, cell_coords):
        self.board[cell_coords[0]][cell_coords[1]] = (self.board[cell_coords[0]][cell_coords[1]] + 1) % 3

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        return cell

    def getflag(self):
        return self.flag
    
    def setflag(self):
        self.flag = True
        return True

    def resetflag(self):
        self.flag = False
        return False

    def get_board(self, x, y):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.board[x][y]
        else:
            return 0


######################################################################
#     ОСНОВНОЙ ИГРОВОЙ КЛАСС SEA
######################################################################
class Sea(Board):
    """
    Класс реализующий игровое поле для каждого участника игры
    """
    # ---------------------------------------------------------------------------
    def __init__(self, num):
        super().__init__(10, 10)
        super().set_view(60 + 12 * 40 * num, 150, 40)
        self.num = num
        self.explore = []  # фазы взрыва
        for i in range(1, 11):
            fname = f'phase{i:02}.png'
            self.explore.append(pygame.transform.scale(load_image(fname), (self.cell_size, self.cell_size)))
        self.queue = []
        self.move = 0
        self.next_move = 0, 0
        self.last_shot = False
        self.last_coord = None
        self.move_queue = []
        self.fog = True

    def shot(self):
        """
        Фиксация результатов выстрела по выбранным координатам
        """
        self.on_click(self.next_move)

    # ---------------------------------------------------------------------------
    def add_explore(self, x, y):
        """
        Дополнение очереди полей, на которых происходит анимация взврыва
        :param x:  Номер столбца ячейки
        :param y:  Номер строки ячейки
        :return:
        """
        self.queue.append((0, x, y))

    # ---------------------------------------------------------------------------
    def score(self):
        """
        Подсчет количества не подбитых секций кораблей
        :return:  - количество секций
        """
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                count += self.board[x][y] == 10
        if count == 0:
            self.boardcolor = 'gray'
        else:
            self.boardcolor = 'black'
        return count

    # ---------------------------------------------------------------------------
    def fill(self, coords):
        """
        Заполнение игрового поля кораблями по координатам из множества coords
        :param coords:
        :return:
        """
        for x in range(10):
            for y in range(10):
                self.board[x][y] = 0
        for crd in coords:
            self.board[crd[0]][crd[1]] = 10
        self.move = 0
        self.last_shot = False
        self.last_coord = None
        self.move_queue = []
        self.fog = True

    # ---------------------------------------------------------------------------
    def render(self, screen):
        """
        Отрисовка игрового поля и игровой ситуации
        :param screen:
        :return:
        """
        super().render(screen)
        font = pygame.font.Font(None, 50)
        if self.num:
            word = 'робот'
        else:
            word = 'игрок'
        text = font.render(f"{word}: {self.score()}", True, 'blue')
        screen.blit(text, (self.left + 3 * self.cell_size,
                           self.top - 50))
        font = pygame.font.Font(None, 30)
        for x in range(10):
            text = font.render(f"{chr(x + ord('А'))}", True, self.boardcolor)
            screen.blit(text, (self.left + x * self.cell_size + self.cell_size // 3,
                               self.top + 5 + self.cell_size * 10))
        for y in range(10):
            text = font.render(f"{y + 1:2}", True, self.boardcolor)
            screen.blit(text, (self.left - 26,
                               self.top + y * self.cell_size + self.cell_size // 3))
        for x in range(10):
            for y in range(10):
                if self.board[x][y] in {0, 10} and self.num == 1 and self.fog:
                    screen.fill('gray', (self.left + x * self.cell_size + 2,
                                         self.top + y * self.cell_size + 2,
                                         self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] == 10 and self.num == 0 and self.fog:
                    screen.fill('black', (self.left + x * self.cell_size + 2,
                                          self.top + y * self.cell_size + 2,
                                          self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] == 10 and not self.fog:
                    screen.fill('green', (self.left + x * self.cell_size + 2,
                                          self.top + y * self.cell_size + 2,
                                          self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] == 11:
                    screen.fill('red', (self.left + x * self.cell_size + 2,
                                        self.top + y * self.cell_size + 2,
                                        self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] == 12:
                    screen.fill('brown', (self.left + x * self.cell_size + 2,
                                          self.top + y * self.cell_size + 2,
                                          self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] in {1, 11, 12}:
                    pygame.draw.line(screen, 'gray', (self.left + x * self.cell_size + 6,
                                                      self.top + y * self.cell_size + 6),
                                     (self.left + (x + 1) * self.cell_size - 6,
                                      self.top + (y + 1) * self.cell_size - 6), width=5)
                    pygame.draw.line(screen, 'gray', (self.left + (x + 1) * self.cell_size - 6,
                                                      self.top + y * self.cell_size + 6),
                                     (self.left + x * self.cell_size + 6,
                                      self.top + (y + 1) * self.cell_size - 6), width=5)
        tque = []
        for exp in self.queue:
            screen.blit(self.explore[exp[0] // 2], (self.left + exp[1] * self.cell_size + 2,
                                                    self.top + exp[2] * self.cell_size + 2))
            if exp[0] < 19:
                tque.append((exp[0] + 1, exp[1], exp[2]))
            self.queue = tque[:]

    # ---------------------------------------------------------------------------
    def check(self, ship, area, x, y):
        """
        Рекурсивный обход полей вогруг выстрела для проверки на полное потопление корабля
        :param ship:
        :param area:
        :param x:
        :param y:
        :return:
        """
        if (x, y) in area:
            return 0
        else:
            if 0 <= x < self.width and 0 <= y < self.height:
                area.add((x, y))
            if self.get_board(x, y) >= 10:
                ship.add((x, y))
                sm = self.get_board(x, y) == 10
                sm += self.check(ship, area, x - 1, y)
                sm += self.check(ship, area, x + 1, y)
                sm += self.check(ship, area, x, y - 1)
                sm += self.check(ship, area, x, y + 1)
                sm += self.check(ship, area, x - 1, y - 1)
                sm += self.check(ship, area, x + 1, y - 1)
                sm += self.check(ship, area, x + 1, y + 1)
                sm += self.check(ship, area, x - 1, y + 1)
                return sm
            else:
                return 0

    # ---------------------------------------------------------------------------
    def on_click(self, cell_coords):
        """
        Анализ поля, в которое произошел выстрел
        :param cell_coords:
        :return:
        """
        curr = self.board[cell_coords[0]][cell_coords[1]]
        if curr in {0, 10, 11}:
            self.move += 1
        if curr in {0, 10}:
            if curr == 10:
                self.last_coord = cell_coords
                self.last_shot = True
                self.move_queue.append(cell_coords)
                play_sound('explore01.ogg')
            else:
                play_sound('explore00.ogg')
            self.add_explore(cell_coords[0], cell_coords[1])
            self.board[cell_coords[0]][cell_coords[1]] += 1
        curr = self.board[cell_coords[0]][cell_coords[1]]
        if curr == 11:
            x = cell_coords[0]
            y = cell_coords[1]
            area = set()
            ship = set()
            if self.check(ship, area, x, y) == 0:
                area = area - ship
                self.last_coord = None
                self.last_shot = False
                play_sound('explore02.ogg')
                for block in ship:
                    self.add_explore(block[0], block[1])
                    self.board[block[0]][block[1]] = 12
                for block in area:
                    self.board[block[0]][block[1]] = 1
