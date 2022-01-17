from configparser import ConfigParser

import pygame.event

from modules.ai import AI
from modules.base import Sea
from modules.classes import *
from modules.sql_games import *


def main():
    # --------------------- Инициализация игорового движка ----------------------
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    pygame.init()
    pygame.display.set_caption('Морской бой')
    pygame.mouse.set_visible(False)  # hide the cursor
    load_music(P.music_0, P.M_VOLUME)
    change_music(True)
    clock = pygame.time.Clock()
    if P.WIN_STAT == 'fullscreen':
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)
    # ----- SPLASH SCREEN ----------------------------
    pygame.time.set_timer(pygame.USEREVENT + 1, TIMER_SPLASH)
    text_info = [' Сыграй с жуликом и победи!',
                 'Противник делает ход каждые',
                 f'   {P.DOP_SHOT // 1000} секунды вне очереди',
                 ' и каждый раз после тебя...',
                 '',
                 '',
                 '  НАЖМИ ЛЮБУЮ КНОПКУ']
    img0 = load_image('title.png')
    SplashBoat(100, 400, load_image('ship02.PNG'))
    boat02 = SplashBoat(850, 400, load_image('ship01.png'))
    boom = Cursor('explore02.png', 8, 4)
    shot = None
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                cont = False
            if event.type == (pygame.USEREVENT + 1):
                shot = SplashShot(150, 500)
        screen.fill('blue')
        font = pygame.font.Font(None, 50)
        splash_sprites.update()
        splash_sprites.draw(screen)
        if shot and boom.frame == 0 and pygame.sprite.collide_mask(boat02, shot):
            play_sound('explore02.ogg')
            boom.move((shot.rect.x, shot.rect.y), 0)
            shot.kill()
            shot = None
            boom.shot()
        step = 50
        left = 400
        for i in range(len(text_info)):
            string = font.render(text_info[i], True, 'white')
            screen.blit(string, (left, step * i + 300))
        screen.blit(img0, (185, 20))
        pygame.display.flip()
        clock.tick(FPS0)
    # ----- SPLASH SCREEN END ----------------------------
    pygame.time.set_timer(pygame.USEREVENT, P.DOP_SHOT)
    load_music(P.music_1, P.M_VOLUME)
    music_state = change_music(True)
    field1 = Sea(0)
    field1.fill(AI().get_coords())
    field2 = Sea(1)
    field2.fill(AI().get_coords())
    spr01 = Button(width - 270, 30, 'ЗАНОВО', 1)  # uid = 1
    spr02 = Button(width - 270, 140, 'МУЗЫКА', 2)  # uid = 2
    spr03 = Button(width - 270, 250, ' ВЫХОД')  # uid = 0
    spr04 = Boat(10, 10, 'ship02.PNG', 3)  # uid = 3
    spr05 = Boat(900, height - 150, 'ship01.png', 4)  # uid = 4
    sprites = [spr01, spr02, spr04, spr05]
    # Курсоры
    cursor_player = Cursor('mortira.png', 4, 2)  # Курсор игрока
    cursor_ai = Cursor('targets.png', 4, 2)  # Курсор компьютера

    running = True
    gaming = True
    newgame = True
    bright = P.GR_LOW
    queue_clk = []  # Последовательность кликов средней кнопкой мыши для "пасхалки"
    # --------------------- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ------------------------
    while running:
        bright = BrightCounter.count(gaming)
        # ------ Начало отрисовки следующего экрана --------------
        screen.fill((bright, bright, bright + 20))
        win_screen(screen, field1.score(), field2.score(), field1.move, field2.move)
        show_stat(screen, "(ПРОБЕЛ - новая игра, M - музыка on/off)")
        # --------------------------------------------------------
        if (field1.score() == 0 or field2.score() == 0) and gaming:  # --- ЕСТЬ ПОБЕДИТЕЛЬ!!! ---
            add_score(field1.score(), field2.score(), field1.move, field2.move)  # Сохранение итогов игры
            gaming = False
            field1.fog = False
            field2.fog = False
            if field1.score() == 0:
                load_music(P.music_0, 1)
            else:
                load_music(P.music_2, 1)
            music_state = change_music(True)
        # --------- Цикл обработки событий ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.time.set_timer(pygame.USEREVENT + 4, FPS)  # Секундная задержка перед завершением игры
            if event.type == pygame.USEREVENT + 4:
                running = False
                gaming = False
            if event.type in (pygame.USEREVENT, pygame.USEREVENT + 2):  # Срабатывание таймеров хода AI
                if gaming:
                    if event.type == pygame.USEREVENT:
                        pygame.time.set_timer(pygame.USEREVENT, P.DOP_SHOT)
                        pygame.time.set_timer(pygame.USEREVENT + 2, TIME_AI_MOVE)
                        cursor_ai.move(ai_move(field1), TIME_AI_MOVE)  # Основной и Дополнительный ход компьютера
                    else:
                        pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                        cursor_ai.shot()
                        field1.shot()
                        field2.resetflag()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Обработка клика мыши
                if event.button == 2:  # Средняя кнопка мыши
                    for obj in sprites:
                        if obj.check_click(event.pos):
                            queue_clk.append(obj.uid)
                    if spr03.check_click(event.pos):
                        queue_clk = []
                    if queue_clk == FOG_OFF:  # Отключение "тумана войны" по совпадению последовательности
                        field2.fog = False
                        queue_clk = []
                    else:
                        field2.fog = True
                if event.button == 1:  # Левая кнопка мыши
                    if spr01.check_click(event.pos):  # Кнопка "ЗАНОВО"
                        newgame = True
                    elif spr02.check_click(event.pos):  # Кнопка "МУЗЫКА"
                        music_state = change_music(music_state)
                    elif spr03.check_click(event.pos):  # Кнопка "ВЫХОД"
                        pygame.time.set_timer(pygame.USEREVENT + 4, FPS)
                    elif gaming:
                        move = field2.move
                        if not field2.getflag() and field2.get_click(event.pos):
                            if move < field2.move:
                                cursor_player.shot()
                                field2.setflag()
                                pygame.time.set_timer(pygame.USEREVENT + 2, TIME_AI_MOVE)
                                cursor_ai.move(ai_move(field1), TIME_AI_MOVE)  # Ход компьютера и передача координат
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_state = change_music(music_state)
                if event.key == pygame.K_SPACE:
                    newgame = True
        if newgame:
            load_music(P.music_1, P.M_VOLUME)
            music_state = change_music(True)
            gaming = False
            c = True
            while c:
                bright = BrightCounter.count(gaming)
                for event0 in pygame.event.get():
                    if event0.type == pygame.KEYDOWN:
                        c = False
                screen.fill((bright, bright, bright + 20))
                field1.fill(AI().get_coords())
                field2.fill(AI().get_coords())
                field1.fog = False
                field2.fog = False
                field1.render(screen)  # Отрисовка игрового поля 1
                field2.render(screen)  # Отрисовка игрового поля 2
                show_stat(screen, "Для начала игры - нажмите любую клавишу")
                clock.tick(FPS // 4)
                pygame.display.flip()
            field1.fog = True
            field2.fog = True
            gaming = True
            newgame = False
        # ------ Конец цикла обработки событий -------

        cursor_player.move(pygame.mouse.get_pos(), 0)  # Передача координат мыши курсору игрока
        game_sprites.draw(screen)  # Отрисовка спрайтов нижнего слоя
        game_sprites.update()  # Просчёт спрайтов нижнего слова
        field1.render(screen)  # Отрисовка игрового поля 1
        field2.render(screen)  # Отрисовка игрового поля 2
        cursor_sprites.draw(screen)  # Отрисовка спрайтов верхнего слоя
        cursor_sprites.update()  # Просчёт спрайтов верхнего слова
        clock.tick(FPS)
        pygame.display.flip()
        # ---------------------------------------------------------------------------------


if __name__ == '__main__':
    config = ConfigParser()  # создаём объект парсера
    config.read("settings.ini")  # читаем конфиг
    P.config_parse(config)
    main()
    terminate()
