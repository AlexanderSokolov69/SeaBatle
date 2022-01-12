import random
import pygame
from base import Sea
from ai import AI


# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
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
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    pygame.init()

    pygame.display.set_caption('Морской бой')
    pygame.mixer.music.load("music.mp3")
    clock = pygame.time.Clock()
    fps = 30
    pygame.mixer.music.set_volume(0.5)
    music_state = change_music(True)
    running = True
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    pygame.time.set_timer(pygame.USEREVENT, 1500)
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
    pygame.quit()

