import pygame
from base import Board
import random
from ai import AI


class Sea(Board):
    def __init__(self, num):
        super().__init__(10, 10)
        super().set_view(60 + 12 * 40 * num, 150, 40)
        self.num = num
        count = 0

    def score(self):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                count += self.board[x][y] == 10
        if count == 0:
            self.boardcolor = 'gray'
        else:
            self.boardcolor = 'black'
        return  count

    def fill(self, coords):
        for x in range(10):
            for y in range(10):
                self.board[x][y] = 0
        for crd in coords:
            self.board[crd[0]][crd[1]] = 10

    def render(self, screen):
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
            text = font.render(f"{x}", True, self.boardcolor)
            screen.blit(text, (self.left + x * self.cell_size + self.cell_size // 3,
                               self.top + 5 + self.cell_size * 10))
        for y in range(10):
            text = font.render(f"{y}", True, self.boardcolor)
            screen.blit(text, (self.left - 20,
                               self.top + y * self.cell_size + self.cell_size // 3))
        for x in range(10):
            for y in range(10):
                if self.board[x][y] in {0, 10} and self.num == 1:
                    screen.fill('gray', (self.left + x * self.cell_size + 2,
                                 self.top + y * self.cell_size + 2,
                                 self.cell_size - 4, self.cell_size - 4))
                if self.board[x][y] == 10 and self.num == 0:
                    screen.fill('black', (self.left + x * self.cell_size + 2,
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


    def check(self, ship, area, x, y):
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

    def on_click(self, cell_coords):
        curr = self.board[cell_coords[0]][cell_coords[1]]
        if curr in {0, 10}:
            self.board[cell_coords[0]][cell_coords[1]] += 1
        curr = self.board[cell_coords[0]][cell_coords[1]]
        if curr == 11:
            x = cell_coords[0]
            y = cell_coords[1]
            area = set()
            ship = set()
            if self.check(ship, area, x, y) == 0:
                area = area - ship
                for block in ship:
                    self.board[block[0]][block[1]] = 12
                for block in area:
                    self.board[block[0]][block[1]] = 1


def show_stat(screen):
    font = pygame.font.Font(None, 60)
    text = font.render("Sea Battle", True, 'red')
    screen.blit(text, (400, 5))
    font = pygame.font.Font(None, 30)
    text = font.render("(SPACE - new game)", True, 'brown')
    screen.blit(text, (410, 50))

def AI_move(board):
    if board.score() > 0:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        while board.board[x][y] in {1, 11, 12}:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        board.on_click((x, y))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Морской бой')
    clock = pygame.time.Clock()
    fps = 50
    running = True
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(pygame.USEREVENT, 1500)
    field1 = Sea(0)
    a1 = AI()
    field1.fill(a1.get_coords())
    field2 = Sea(1)
    a2 = AI()
    field2.fill(a2.get_coords())
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
        if field1.score() == 0 or field2.score() == 0:
            gaming = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if gaming:
                    AI_move(field1)
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
                if event.key == pygame.K_SPACE:
                    a = AI()
                    field1.fill(a.get_coords())
                    a = AI()
                    field2.fill(a.get_coords())
                    gaming = True

        field1.render(screen)
        field2.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
