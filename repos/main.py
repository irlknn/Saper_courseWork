import customtkinter as ctk
from menu import MainMenu
from constants import *

def main():
    # Кольорова тема
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("D:\\courseWork\\repos\\themes\\custom_theme.json")  

    # створення основного вікна
    root = ctk.CTk()
    root.title("Меню гри Сапер") 
    root.geometry(MAIN_MENU_SIZE)
    MainMenu(root)

    root.mainloop()

if __name__ == "__main__":
    main()
