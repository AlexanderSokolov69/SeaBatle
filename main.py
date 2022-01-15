import configparser

from modules.ai import AI
from modules.base import Sea
from modules.classes import *
from modules.ingame import *
from modules.sql_games import add_score


def main():
    # --------------------- Инициализация игорового движка ----------------------
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512, devicename=None)
    pygame.init()
    pygame.display.set_caption('Морской бой')
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
                 '         PRESS ANY KEY']
    img0 = load_image('title.png')
    SplashBoat(100, 400, load_image('ship02.PNG'))
    SplashBoat(850, 400, load_image('ship01.png'))
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                cont = False
            if event.type == (pygame.USEREVENT + 1):
                SplashShot(150, 500)
        screen.fill('blue')
        font = pygame.font.Font(None, 50)
        splash_sprites.draw(screen)
        splash_sprites.update()
        step = 50
        left = 400
        for i in range(len(text_info)):
            string = font.render(text_info[i], True, 'white')
            screen.blit(string, (left, step * i + 300))
        screen.blit(img0, (250, 20))
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
    spr01 = Button(width - 270, 30, 'ЗАНОВО')
    spr02 = Button(width - 270, 140, 'МУЗЫКА')
    spr03 = Button(width - 270, 250, ' ВЫХОД')
    Boat(10, 10, 'ship02.PNG')
    Boat(900, height - 150, 'ship01.png')
    running = True
    darkout = True
    gaming = True
    gr = P.GR_LOW
    step = BR_STEP
    while darkout or running:
        if gaming:
            if gr < GR_HIGH:
                gr += BR_STEP
            darkout = True
        else:
            if gr >= GR_HIGH:
                step = -2
            if gr < P.GR_LOW:
                step = 0
                darkout = False
            gr += step
        screen.fill((gr, gr, gr))
        win_screen(screen, field1.score(), field2.score(), field1.move, field2.move)
        show_stat(screen)
        if (field1.score() == 0 or field2.score() == 0) and gaming:
            gaming = False
            if field1.score() == 0:
                load_music(P.music_0, 1)
            else:
                load_music(P.music_2, 1)
            music_state = change_music(True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gaming = False
                add_score(field1.score(), field2.score(), field1.move, field2.move)
            if event.type in (pygame.USEREVENT, pygame.USEREVENT + 2):
                if gaming:
                    pygame.time.set_timer(pygame.USEREVENT, P.DOP_SHOT)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                    ai_move(field1)  # Основной и Дополнительный ход компьютера
                    field2.resetflag()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if spr01.check_click(event.pos):
                        add_score(field1.score(), field2.score(), field1.move, field2.move)
                        load_music(P.music_1, P.M_VOLUME)
                        music_state = change_music(True)
                        field1.fill(AI().get_coords())
                        field2.fill(AI().get_coords())
                        gaming = True
                    elif spr02.check_click(event.pos):
                        music_state = change_music(music_state)
                    elif spr03.check_click(event.pos):
                        running = False
                        gaming = False
                    elif gaming:
                        move = field2.move
                        if not field2.getflag() and field2.get_click(event.pos):
                            if move < field2.move:
                                field2.setflag()
                                pygame.time.set_timer(pygame.USEREVENT + 2, 500)
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    music_state = change_music(music_state)
                if event.key == pygame.K_SPACE:
                    add_score(field1.score(), field2.score(), field1.move, field2.move)
                    load_music(P.music_1, P.M_VOLUME)
                    music_state = change_music(True)
                    field1.fill(AI().get_coords())
                    field2.fill(AI().get_coords())
                    gaming = True
        
        field1.render(screen)
        field2.render(screen)
        game_sprites.draw(screen)
        game_sprites.update()
        
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    config = configparser.ConfigParser()  # создаём объект парсера
    config.read("settings.ini")  # читаем конфиг
    P.config_parse(config)
    main()
    terminate()
