import threading
from game import *
from settings_menu import SettingsMenu
from constants import *
import customtkinter as ctk

class MainMenu:
    def __init__(self, root):
        self.root = root

        self.rows = STANDART_ROW_AMOUNT
        self.cols = STANDART_COLS_AMOUNT
        self.mines = STANDART_MINES_AMOUNT

        # Головне меню
        self.title = ctk.CTkLabel(self.root, text=TITLE, font=(FONT, 32, "bold"))
        self.title.pack(pady=50)

        # Кнопка почати гру
        self.start_button = ctk.CTkButton(self.root, text="почати гру", font=(FONT, TEXT_SIZE), command=self.start_game, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.start_button.pack(pady=20)

        # Кнопка налаштування
        self.settings_button = ctk.CTkButton(self.root, text="налаштування", font=(FONT, TEXT_SIZE), command=self.show_settings, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.settings_button.pack(pady=20)

        # Кнопка вихід
        self.exit_button = ctk.CTkButton(self.root, text="вихід", font=(FONT, TEXT_SIZE), command=self.exit_game, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        self.exit_button.pack(pady=20)

        # пустий фрейму для налаштувань
        self.settings_frame = None

    def disable_buttons(self):
        self.start_button.configure(state='disabled')
        self.settings_button.configure(state='disabled')
        self.exit_button.configure(state='disabled')

    def enable_buttons(self):
        self.start_button.configure(state='normal')
        self.settings_button.configure(state='normal')
        self.exit_button.configure(state='normal')

    def start_game(self):
        self.disable_buttons()
        # створення окремого потоку для гри
        self.game_thread = threading.Thread(target=self.run_game)
        self.game_thread.start()

    def run_game(self):
        self.a, self.b = 0,0
        game = Game(self, self.a, self.b)
        while True:
            game.new()
            game.run()

    def show_settings(self):
        # приховування кнопок меню
        self.title.pack_forget()
        self.start_button.pack_forget()
        self.settings_button.pack_forget()
        self.exit_button.pack_forget()

        # спільний фрейм для налаштувань, якщо він ще не був створений
        if self.settings_frame is None:
            settings_menu = SettingsMenu(self.root, self)
            settings_menu.create_menu()

    def exit_game(self):
        if hasattr(self, 'game_thread') and self.game_thread.is_alive():
            self.game_thread.join()  # Чекаємо завершення потоку

        pygame.quit()
        self.root.quit()
        quit(0)

        