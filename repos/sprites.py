import random
import pygame
from constants import *

class TileStruct(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_char),
        ("adjacentMines", ctypes.c_int)
    ]

# оголошення функції з cpp бібліотеки 
clibrary.create_board.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
clibrary.create_board.restype = ctypes.POINTER(TileStruct)

class Tile:
    def __init__(self, x, y, tile_type, adjacent_mines):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.type = tile_type
        self.adjacentMines = adjacent_mines
        self.image = tile_unknown
        self.revealed = False
        self.flagged = False

    def draw(self, board_surface):
        if not self.flagged and self.revealed:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.flagged and not self.revealed:
            board_surface.blit(tile_flag, (self.x, self.y))
        elif not self.revealed:
            board_surface.blit(tile_unknown, (self.x, self.y))

    def __repr__(self):
        return self.type.decode()

class Board():
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board_surface = pygame.Surface((TILE_SIZE * rows, TILE_SIZE * cols))
        self.board_list = self.load_board()
        self.dug = []
        
    def load_board(self):
        size = ctypes.c_int()
        board_ptr = clibrary.create_board(self.rows, self.cols, self.mines, ctypes.byref(size))
        tiles = ctypes.cast(board_ptr, ctypes.POINTER(TileStruct * size.value)).contents

        # конвертування з одновимірного масиву в двохвимірний
        board = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                tile = tiles[r * self.cols + c]
                # вибір зображення зі словника
                if tile.type == b'C' and tile.adjacentMines > 0:
                    tile.image = tile_numbers[tile.adjacentMines - 1]
                else:
                    # не відкрита клітинка за замовчуванням
                    tile.image = tile_images.get(tile.type, tile_unknown)  
                row.append(Tile(r, c, tile.type, tile.adjacentMines))
            board.append(row)

        return board

    def dig(self, x, y):
        # уникнення повторного виклику
        if (x, y) in self.dug:  
            return True

        # стек для обробки клітинок
        stack = [(x, y)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in self.dug:
                continue

            tile = self.board_list[cx][cy]
            tile.revealed = True
            self.dug.append((cx, cy))

            if tile.type == b'X':  # якщо це міна
                tile.image = tile_exploded
                return False
            elif tile.type == b'C':  # якщо це клітинка з підказкою
                tile.image = tile_numbers[tile.adjacentMines - 1]
            elif tile.type == b'/':  # якщо це порожня клітинка
                tile.image = tile_empty
                for row in range(max(0, cx-1), min(self.rows, cx+2)):
                    for col in range(max(0, cy-1), min(self.cols, cy+2)):
                        if (row, col) not in self.dug:
                            # додаємо сусідні клітинки до стеку
                            stack.append((row, col))

        return True

    def draw(self, screen, camera_x, camera_y):
        for row in self.board_list:
            for tile in row:
                tile.draw(self.board_surface)

        surface = pygame.display.get_surface() 
        x,y = surface.get_width(), surface.get_height()

        visible_area = pygame.Rect(camera_x, camera_y, x, y)

        # зображується лише видима для користувача частина поля
        screen.blit(self.board_surface, (0, 0), visible_area)

