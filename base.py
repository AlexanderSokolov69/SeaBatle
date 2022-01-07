import pygame

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * height for _ in range(width)]
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

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                    pygame.draw.rect(screen, self.boardcolor,
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), width=1)

    def get_cell(self, mouse_pos):
        if self.left < mouse_pos[0] < self.left + self.cell_size * self.width and \
            self.top < mouse_pos[1] < self.top + self.cell_size * self.height:
            return ((mouse_pos[0] - self.left) // self.cell_size,
                    (mouse_pos[1] - self.top) // self.cell_size)

    def on_click(self, cell_coords):
        self.board[cell_coords[0]][cell_coords[1]] = (self.board[cell_coords[0]][cell_coords[1]] + 1) % 3

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.flag = True
            self.on_click(cell)

    def getflag(self):
        res = self.flag
        self.resetflag()
        return res

    def resetflag(self):
        self.flag = False

    def get_board(self, x, y):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.board[x][y]
        else:
            return 0
