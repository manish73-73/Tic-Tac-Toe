from tkinter import *
import numpy as np

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.reset_game()

    def reset_game(self):
        self.canvas.delete("all")
        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros((3, 3))
        self.game_over = False
        self.scores = {'X': 0, 'O': 0, 'Tie': 0}

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(1, 3):
            self.canvas.create_line(i * size_of_board / 3, 0, i * size_of_board / 3, size_of_board)
            self.canvas.create_line(0, i * size_of_board / 3, size_of_board, i * size_of_board / 3)

    def draw_symbol(self, logical_position, symbol):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if symbol == 'X':
            self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                    grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                    width=symbol_thickness, fill=symbol_X_color)
            self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                    grid_position[0] + symbol_size, grid_position[1] - symbol_size,
                                    width=symbol_thickness, fill=symbol_X_color)
        else:
            self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                    grid_position[0] + symbol_size, grid_position[1] + symbol_size,
                                    width=symbol_thickness, outline=symbol_O_color)

    def display_game_over(self):
        if self.game_over:
            text = 'Game Over: '
            if self.is_winner('X'):
                text += 'Player 1 (X) Wins!'
                self.scores['X'] += 1
            elif self.is_winner('O'):
                text += 'Player 2 (O) Wins!'
                self.scores['O'] += 1
            else:
                text += 'It\'s a Tie!'
                self.scores['Tie'] += 1

            self.canvas.delete("all")
            self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 30 bold", fill="black", text=text)
            self.canvas.create_text(size_of_board / 2, 2 * size_of_board / 3, font="cmr 20 bold",
                                    text=f"Scores: X={self.scores['X']} O={self.scores['O']} Tie={self.scores['Tie']}")
            self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 6, font="cmr 20 bold",
                                    text='Click to Play Again')

    def convert_logical_to_grid_position(self, logical_position):
        return (size_of_board / 3) * np.array(logical_position, dtype=int) + size_of_board / 6

    def is_grid_occupied(self, logical_position):
        return self.board_status[tuple(logical_position)] != 0

    def is_winner(self, player):
        player_value = -1 if player == 'X' else 1
        return any(np.all(self.board_status[i, :] == player_value) for i in range(3)) or \
               any(np.all(self.board_status[:, i] == player_value) for i in range(3)) or \
               np.all(np.diag(self.board_status) == player_value) or \
               np.all(np.diag(np.fliplr(self.board_status)) == player_value)

    def is_game_over(self):
        self.game_over = self.is_winner('X') or self.is_winner('O') or not np.any(self.board_status == 0)
        return self.game_over

    def click(self, event):
        if self.game_over:
            self.reset_game()
            return

        logical_position = [event.x // (size_of_board // 3), event.y // (size_of_board // 3)]
        if not self.is_grid_occupied(logical_position):
            symbol = 'X' if self.player_X_turns else 'O'
            self.draw_symbol(logical_position, symbol)
            self.board_status[tuple(logical_position)] = -1 if symbol == 'X' else 1
            self.player_X_turns = not self.player_X_turns

            if self.is_game_over():
                self.display_game_over()

game_instance = TicTacToe()
game_instance.mainloop()
