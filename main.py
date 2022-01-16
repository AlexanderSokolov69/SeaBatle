from configparser import ConfigParser

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
    shot = SplashBoat(100, 400, load_image('ship02.PNG'))
    boat02 = SplashBoat(850, 400, load_image('ship01.png'))
    boom = Cursor('explore02.png', 8, 4)
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                cont = False
            if event.type == (pygame.USEREVENT + 1):
                boom.move((150, 500), 0)
                boom.shot()
                # shot = SplashShot(150, 500)
        screen.fill('blue')
        font = pygame.font.Font(None, 50)
        splash_sprites.draw(screen)
        splash_sprites.update()
        if pygame.sprite.collide_mask(boat02, shot):
            pass
        #     # explore.shot()
        #     explore.move((shot.rect.x, shot.rect.y), 500)
        #     shot.kill()
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
    spr01 = Button(width - 270, 30, 'ЗАНОВО', 1)
    spr02 = Button(width - 270, 140, 'МУЗЫКА', 2)
    spr03 = Button(width - 270, 250, ' ВЫХОД')
    spr04 = Boat(10, 10, 'ship02.PNG', 3)
    spr05 = Boat(900, height - 150, 'ship01.png', 4)
    sprites = [spr01, spr02, spr04, spr05]
    # Курсоры
    cursor_player = Cursor('mortira.png', 4, 2)  # Курсор игрока
    cursor_ai = Cursor('targets.png', 4, 2)  # Курсор компьютера

    running = True
    gaming = True
    gr = P.GR_LOW
    step = BR_STEP
    queue_clk = []
    # --------------------- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ ------------------------
    while running:
        if gaming:
            if gr < GR_HIGH:
                gr += BR_STEP
        else:
            if gr >= GR_HIGH:
                step = -2
            if gr < P.GR_LOW:
                step = 0
            gr += step
        # ------ Начало отрисовки следующего экрана --------------
        screen.fill((gr, gr, gr + 20))
        win_screen(screen, field1.score(), field2.score(), field1.move, field2.move)
        show_stat(screen)
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
                        load_music(P.music_1, P.M_VOLUME)
                        music_state = change_music(True)
                        field1.fill(AI().get_coords())
                        field2.fill(AI().get_coords())
                        gaming = True
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
                    load_music(P.music_1, P.M_VOLUME)
                    music_state = change_music(True)
                    field1.fill(AI().get_coords())
                    field2.fill(AI().get_coords())
                    gaming = True
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
