from game import *
from constants import *
import customtkinter as ctk

TEXT_SIZE = 24
mode = "light"

class SettingsMenu:
    def __init__(self, root, main_menu):
        self.main_menu = main_menu
        self.settings_frame = ctk.CTkFrame(root)

        self.rows = main_menu.rows
        self.cols = main_menu.cols
        self.mines = main_menu.mines

    def create_menu(self):
        settings_label = ctk.CTkLabel(self.settings_frame, text="Налаштування", font=(FONT, 28, "bold"))
        settings_label.grid(row=0, column=1, pady=20)

        self.rows_change()
        self.cols_change()
        self.mines_change()
        self.theme_change()
        self.back_button()

        # Відображаємо фрейм з налаштуваннями
        self.settings_frame.place(relx=0.5, rely=0.5, anchor="center")

    def destroy_lable(self):
        if self.output_label:
            self.output_label.destroy()

    # віджети для зміни кількості рядків
    def rows_change(self):
        row_lable = ctk.CTkLabel(self.settings_frame, text='Кількість стовпців: ', font=(FONT, TEXT_SIZE))
        row_lable.grid(row=1, column=0, padx=10, pady=10)
        
        entry_rows = ctk.CTkEntry(self.settings_frame, height=50, width=200, corner_radius=20)
        entry_rows.grid(row=1, column=1, padx=10, pady=10)

        self.output_label = None

        def get_rows():
            input_rows = entry_rows.get()
            self.destroy_lable()

            if input_rows.isdigit():
                if int(input_rows) > 200:
                    self.output_label = ctk.CTkLabel(self.settings_frame, text="Максимальна допустима розмірність поля - 200x200")
                    self.output_label.grid(row=4, column=1)
                    self.rows = STANDART_ROW_AMOUNT
                    return
                self.output_label = ctk.CTkLabel(self.settings_frame, text="Кількість стовпців збережена")
                self.rows = int(input_rows)
            else:
                self.output_label = ctk.CTkLabel(self.settings_frame, text="Помилка, введіть ціле, додатнє число")
                self.rows = STANDART_ROW_AMOUNT

            self.output_label.grid(row=4, column=1)

        # Кнопка для збереження змін кількості рядків
        save_button_row = ctk.CTkButton(self.settings_frame, text="Зберегти", font=(FONT, TEXT_SIZE), command=get_rows)
        save_button_row.grid(row=1, column=2, padx=10, pady=10)


    # віджети для зміни кількості стовпців
    def cols_change(self):
        col_lable = ctk.CTkLabel(self.settings_frame, text='Кількість рядків: ', font=(FONT, TEXT_SIZE))
        col_lable.grid(row=2, column=0, padx=10, pady=10)
        
        entry_cols = ctk.CTkEntry(self.settings_frame, height=50, width=200, corner_radius=20)
        entry_cols.grid(row=2, column=1, padx=10, pady=10)

        self.output_label = None

        def get_cols():
            input_cols = entry_cols.get()
            self.destroy_lable()
            
            if input_cols.isdigit():
                if int(input_cols) > 200:
                    self.output_label = ctk.CTkLabel(self.settings_frame, text="Максимальна допустима розмірність поля - 200x200")
                    self.output_label.grid(row=4, column=1)
                    self.cols = STANDART_COLS_AMOUNT
                    return
                self.output_label = ctk.CTkLabel(self.settings_frame, text="Кількість рядків збережена")
                self.cols = int(input_cols)
            else:
                self.output_label = ctk.CTkLabel(self.settings_frame, text="Помилка, введіть ціле, додатнє число")
                self.cols = STANDART_COLS_AMOUNT

            self.output_label.grid(row=4, column=1)

        # кнопка для збереження змін кількості стовпців
        save_button_col = ctk.CTkButton(self.settings_frame, text="Зберегти", font=(FONT, TEXT_SIZE), command=get_cols)
        save_button_col.grid(row=2, column=2, padx=10, pady=10)

    # віджети для зміни кількості мін
    def mines_change(self):
        mine_lable = ctk.CTkLabel(self.settings_frame, text='Кількість мін: ', font=(FONT, TEXT_SIZE))
        mine_lable.grid(row=3, column=0, padx=10, pady=10)
        
        entry_mines = ctk.CTkEntry(self.settings_frame, height=50, width=200, corner_radius=20)
        entry_mines.grid(row=3, column=1, padx=10, pady=10)

        self.output_label = None

        def get_mines():
            input_mines = entry_mines.get()
            self.destroy_lable()
            
            if input_mines.isdigit():
                if int(input_mines) <= self.rows * self.cols:
                    self.output_label = ctk.CTkLabel(self.settings_frame, text=f"Кількість мін збережена")
                    self.mines = int(input_mines)
                else:
                    self.output_label = ctk.CTkLabel(self.settings_frame, text="Некоректна кількість мін")
                    self.mines = STANDART_MINES_AMOUNT
            else:
                self.output_label = ctk.CTkLabel(self.settings_frame, text="Помилка, введіть ціле, додатнє число")
                self.mines = STANDART_MINES_AMOUNT

            self.output_label.grid(row=4, column=1)

        # кнопка для збереження змін кількості мін
        save_button_mine = ctk.CTkButton(self.settings_frame, text="Зберегти", font=(FONT, TEXT_SIZE), command=get_mines)
        save_button_mine.grid(row=3, column=2, padx=10, pady=10)

    # кнопка зміни кольорової теми
    def theme_change(self): 
        def change():
            global mode
            if mode == "dark":
                ctk.set_appearance_mode("light")
                mode = "light"
            else:
                ctk.set_appearance_mode("dark")
                mode = "dark"
		        
        theme_button = ctk.CTkButton(self.settings_frame, text="Змінити тему (світла/темна)", command=change, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, font=(FONT, TEXT_SIZE))
        theme_button.grid(row=5, column=1, pady=20)

    # кнопка повернутись назад до меню
    def back_button(self):
        back_button = ctk.CTkButton(self.settings_frame, text="Повернутись назад", font=(FONT, TEXT_SIZE), command=self.return_to_menu, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        back_button.grid(row=6, column=1, pady=20)

    def save_settings(self):
        self.main_menu.rows = self.rows
        self.main_menu.cols = self.cols
        self.main_menu.mines = self.mines

    def return_to_menu(self):
        self.save_settings()
        self.settings_frame.place_forget()

        # Показуємо основне меню
        self.main_menu.title.pack(pady=50)
        self.main_menu.start_button.pack(pady=10)
        self.main_menu.settings_button.pack(pady=10)
        self.main_menu.exit_button.pack(pady=10)
