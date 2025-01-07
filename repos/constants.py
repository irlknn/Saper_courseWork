import ctypes
import pygame
import os

clibrary = ctypes.CDLL("D:\\courseWork\\repos\\cppLibrary\\cpplibrary.dll")

STANDART_ROW_AMOUNT = 10
STANDART_COLS_AMOUNT = 10
STANDART_MINES_AMOUNT = 9
TILE_SIZE = 32
FPS = 60
CAMERA_SPEED = 10

FONT = "Arial"
TEXT_SIZE = 28

MAIN_MENU_SIZE = "800x600" 
TITLE = "сапер"
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BGCOLOUR = "#CDCDB1"

image_path = "D:/courseWork/repos/assets"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join(image_path, f"Tile{i}.jpg")), (TILE_SIZE, TILE_SIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileEmpty.jpg")), (TILE_SIZE, TILE_SIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileExploded.jpg")), (TILE_SIZE, TILE_SIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileFlag.jpg")), (TILE_SIZE, TILE_SIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileMine.jpg")), (TILE_SIZE, TILE_SIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileNotMine.jpg")), (TILE_SIZE, TILE_SIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "TileUnknown.jpg")), (TILE_SIZE, TILE_SIZE))

arrow = pygame.transform.scale(pygame.image.load("D:\\courseWork\\repos\\assets\\row.png"), (40, 40))
        
tile_images = {
    b'X': tile_mine,        # Міна
    b'.': tile_unknown,     # Невідома клітинка
    b'/': tile_empty,       # Порожня клітинка
    b'C': None              # Підказка 
}
    