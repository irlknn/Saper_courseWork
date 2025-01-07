import time
import pygame
from pygame.locals import *

from constants import *  
from sprites import *
from soud_effect import *

class Game:
    def __init__(self, main_menu, win_num, lose_num):
        self.root = main_menu.root  # доступ до вікна меню
        self.rows = main_menu.rows
        self.cols = main_menu.cols
        self.mines = main_menu.mines
        self.main_menu = main_menu

        self.win_num = win_num
        self.lose_num = lose_num

        pygame.init()
        self.board_width = TILE_SIZE * self.rows
        self.board_height = TILE_SIZE * self.cols
        self.screen_width = min(self.board_width, 768)
        self.screen_height = min(self.board_height, 768)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, int(self.screen_width / 15))

        self.camera_x, self.camera_y = 0, 0

        self.start_time, self.end_time = None, None

    def new(self):
        self.board = Board(self.rows, self.cols, self.mines)

    # запуск гри 
    def run(self):
        self.start_time = time.time() # час початку гри 
        self.playing = True
        self.win = False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw_board()
            self.draw_arrow()
            self.root.update()
        self.end_time = time.time() # час закінчення 
        self.end_screen()

    def draw_board(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen, self.camera_x, self.camera_y)
        pygame.display.flip()

    def draw_arrow(self):
        if self.arrow_down:
            arrow_slide()
            arrow_down = pygame.transform.rotate(arrow, -90)
            self.screen.blit(arrow_down, (self.screen_width // 2 - 20, self.screen_height - 50))
            pygame.display.flip()
            
        if self.arrow_up:
            arrow_slide()
            arrow_up = pygame.transform.rotate(arrow, 90)
            self.screen.blit(arrow_up, (self.screen_width // 2 - 20, 10))
            pygame.display.flip()
            
        if self.arrow_left:
            arrow_slide()
            arrow_left = pygame.transform.rotate(arrow, 180)
            self.screen.blit(arrow_left, (10, self.screen_height // 2 - 20))
            pygame.display.flip()
            
        if self.arrow_right:
            arrow_slide()
            arrow_right = arrow
            self.screen.blit(arrow_right, (self.screen_width - 50, self.screen_height // 2 - 20))
            pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != b'X' and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main_menu.enable_buttons()
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # визначення позиції мишки 
                mx, my = pygame.mouse.get_pos()
                mx = (mx + self.camera_x) // TILE_SIZE
                my = (my + self.camera_y) // TILE_SIZE

                # перевірка на межі            
                if not (0 <= mx < self.rows and 0 <= my < self.cols):
                    return

                # при натискані лкм
                if event.button == 1:
                    if self.board.board_list[mx][my].image == tile_unknown:
                        cliking()
                    if not self.board.board_list[mx][my].flagged:   # якщо не позначено
                        if not self.board.dig(mx, my):              # і не відкрите
                            for row in self.board.board_list:       # клітинка відкривається
                                for tile in row:
                                    if tile.flagged and tile.type != b'X':
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == b'X':         # програш при відкриті міни
                                        open_mine()
                                        tile.revealed = True
                            self.playing = False

                # при натискані пкм позначення клітинки прапорцем
                if event.button == 3:
                    if self.board.board_list[mx][my].image == tile_unknown:
                        cliking()
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged

                # перевірка на перемогу
                if self.check_win():
                    # win_sound()
                    self.win = True
                    self.playing = False
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True

        # керування стрілками клавіатури
        keys = pygame.key.get_pressed()
        self.arrow_up = self.arrow_down = self.arrow_left = self.arrow_right = False

        if keys[K_LEFT]:
            self.arrow_left = True
            self.camera_x = max(0, self.camera_x - CAMERA_SPEED)
        if keys[K_RIGHT]:
            self.arrow_right = True
            self.camera_x = min(self.board_width - self.screen_width, self.camera_x + CAMERA_SPEED)
        if keys[K_UP]:
            self.arrow_up = True
            self.camera_y = max(0, self.camera_y - CAMERA_SPEED)
        if keys[K_DOWN]:
            self.arrow_down = True
            self.camera_y = min(self.board_height - self.screen_height, self.camera_y + CAMERA_SPEED)
            

    def end_screen(self):
        if self.win:
            message = "Ви перемогли!"
            color = BLACK
            self.win_num += 1
            self.main_menu.a = self.win_num
        else:
            message = "Ви програли!"
            color = WHITE
            self.lose_num += 1
            self.main_menu.b = self.lose_num

        text_surface = self.font.render(message, True, color)

        spent_time = self.end_time - self.start_time
        time_message = f"Час гри: {int(spent_time // 60)} хв {int(spent_time % 60)} с"
        time_surface = self.font.render(time_message, True, color)

        restart_surface = self.font.render("Натисніть, щоб зіграти ще раз", True, color) 

        score_message = f"Виграли - {self.win_num}р, програли - {self.lose_num}р"
        score_surface = self.font.render(score_message, True, color) 

        # затримка перед виведенням
        pygame.time.delay(900)
        if self.win:
            self.win_screen()
        else:
            self.lose_screen()
            
        self.screen.blit(text_surface, ((self.screen_width - text_surface.get_width()) // 2, self.screen_height // 3.2 ))
        self.screen.blit(score_surface, ((self.screen_width - score_surface.get_width()) // 2, self.screen_height//2.2))
        self.screen.blit(time_surface, ((self.screen_width - time_surface.get_width()) // 2, self.screen_height // 1.9))
        self.screen.blit(restart_surface, ((self.screen_width - restart_surface.get_width()) // 2, self.screen_height // 1.5))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_menu.enable_buttons()
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return 
                
    # вікно при виграші
    def win_screen(self):
        win_sound()
        self.screen.fill(WHITE)
        image_path = "D:\\courseWork\\repos\\end_screen_image\\win_bg.png"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
        x, y = 0, 0
        self.screen.blit(image, (x, y))

    # вікно при програші
    def lose_screen(self):
        lose_sound()
        self.screen.fill(BLACK)
        image_path = "D:\\courseWork\\repos\\end_screen_image\\lose_bg.png"
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
        x, y = 0, 0
        self.screen.blit(image, (x, y))

