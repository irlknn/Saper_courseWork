#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

extern "C"{
    struct Tile {
    char type;  // ".", "X", "C", "/"
    int adjacentMines;

    Tile() : type('.'), adjacentMines(0) {}
    Tile(char t, int mines = 0) : type(t), adjacentMines(mines) {}
    };

    class Board{
        int rows, cols;
        int mineAmount;
        vector <vector<Tile>> board_list;
    
        bool isValidCoord(int row, int col) const {
            return row >= 0 && row < rows && col >= 0 && col < cols;
        }
        
        // Генерація випадкових мін
        void generateMines() {
            vector<pair<int, int>> positions;
            for (int r = 0; r < rows; ++r) {
                for (int c = 0; c < cols; ++c) {
                    positions.emplace_back(r, c);
                }
            }

            // Перемішуємо позиції
            random_shuffle(positions.begin(), positions.end());

            // Розміщуємо міни
            for (int i = 0; i < mineAmount; ++i) {
                int r = positions[i].first;
                int c = positions[i].second;
                board_list[r][c].type = 'X';
            }

            // Підрахунок сусідніх мін для усіх клітинок
            for (int r = 0; r < rows; ++r) {
                for (int c = 0; c < cols; ++c) {
                    if (board_list[r][c].type != 'X') {
                        int count = 0;
                        for (int dr = -1; dr <= 1; ++dr) {
                            for (int dc = -1; dc <= 1; ++dc) {
                                int nr = r + dr;
                                int nc = c + dc;
                                if (isValidCoord(nr, nc) && board_list[nr][nc].type == 'X') {
                                    count++;
                                }
                            }
                        }
                        board_list[r][c].type = (count > 0) ? 'C' : '/';
                        board_list[r][c].adjacentMines = count;
                    }
                }
            }
        }
    public:
        Board(int r, int c, int mines) : rows(r), cols(c), mineAmount(mines){
            board_list.resize(rows, vector<Tile>(cols, Tile()));
            generateMines();
        }
        void toLinearArray(Tile* buffer) const{
            for(int r = 0; r < rows; r++){
                for(int c = 0; c < cols; c++){
                    buffer[r * cols + c] = board_list[r][c];
                }
            }
        }
    };

    Tile* create_board(int rows, int cols, int mines, int* size){
        srand(static_cast<unsigned int>(time(0))); // Ініціалізація генератора випадкових чисел
        Board board(rows, cols, mines);
        int totalSize = rows * cols;
        Tile* buffer = new Tile[totalSize];
        board.toLinearArray(buffer);
        *size = totalSize;
        return buffer;
    }
}
