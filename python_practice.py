import random
import itertools
from datetime import datetime


class Board:
    view_board = [i for i in itertools.repeat(' ', 10)]
    line = '--+---+--'

    def print_board(self):
        return print(
            f'\n{self.view_board[7]} | {self.view_board[8]} | {self.view_board[9]}'
            f'\n{self.line}'
            f'\n{self.view_board[4]} | {self.view_board[5]} | {self.view_board[6]}'
            f'\n{self.line}'
            f'\n{self.view_board[1]} | {self.view_board[2]} | {self.view_board[3]}'
            f'\n'
        )

    def drop_board(self):
        self.view_board = [i for i in itertools.repeat(' ', 10)]
        return self.view_board

    @staticmethod
    def display_main_menu():
        return print(
            '\n|-*-*-*-*-Welcome to the Game-*-*-*-*-|'
            '\n|              Main menu              |'
            '\n|           1 - Start Game            |'
            '\n|           2 - Open the log          |'
            '\n|           3 - Reset log             |'
            '\n|           4 - Exit                  |'
            '\n|-*-*-*-*-*-*-*-*--**--*-*-*-*--*-*-*-|'
        )


class Player:

    def __init__(self):
        self.player_1 = ''
        self.player_2 = ''
        self.player_x_score = 0
        self.player_0_score = 0
        self.choice = ''
        self.marks = {}

    def set_name_players(self):
        print("----------")
        self.player_1 = str(input("Player_1 enter your name: "))
        self.player_2 = str(input("Player_2 enter your name: "))

    def choise_marks(self):

        self.choice = random.randint(0, 1)
        if self.choice == 0:
            self.marks[self.player_1] = 'X'
            self.marks[self.player_2] = '0'
        else:
            self.marks[self.player_1] = '0'
            self.marks[self.player_2] = 'X'
        return print(
            f'{self.player_1} is {self.marks[self.player_1]} and '
            f'{self.player_2} is {self.marks[self.player_2]}')


class Game(Player, Board):
    win_position = [[1, 4, 7], [2, 5, 8], [3, 6, 9], [7, 8, 9], [4, 5, 6], [1, 2, 3], [1, 5, 9], [7, 5, 3]]

    def find_mark_x(self):
        self.player_x = ''.join([key for key, value in self.marks.items() if value == 'X'])
        return self.player_x

    def find_mark_0(self):
        self.player_0 = ''.join([key for key, value in self.marks.items() if value == '0'])
        return self.player_0

    def player_x_turn(self):
        while True:
            position_x = input(f'{self.player_x} pay attention to num lock and choose your position: ')
            if position_x.isdigit() and int(position_x) in range(10):
                position_x = int(position_x)
                if self.view_board[position_x] == " ":
                    return position_x
                else:
                    print('The position has already filled')
            else:
                print('Come on! Where are your concentrate?')

    def player_0_turn(self):
        while True:
            position_0 = input(f'{self.player_0} pay attention to num lock and choose your position: ')
            if position_0.isdigit() and int(position_0) in range(10):
                position_0 = int(position_0)
                if self.view_board[position_0] == " ":
                    return position_0
                else:
                    print('The position has already filled')
            else:
                print('Come on! Where are your concentrate?')

    @staticmethod
    def write_logs(player):
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'\n{datetime.now().strftime("%d-%m-%Y %H:%M")} - won {player}')

    @staticmethod
    def open_logs():
        with open('logs.txt', 'r') as file:
            for line in file:
                print(line, end='')

    def check_winners(self):
        for win in self.win_position:
            if self.view_board[win[0]] == self.view_board[win[1]] == self.view_board[win[2]] == 'X':
                print(f'{self.player_x} is winner')
                self.player_x_score += 1
                self.write_logs(self.player_x)
                if not self.start_new_game():
                    return False
            elif self.view_board[win[0]] == self.view_board[win[1]] == self.view_board[win[2]] == '0':
                print(f'{self.player_0} is winner')
                self.player_x_score += 1
                self.write_logs(self.player_0)
                if not self.start_new_game():
                    return False
        if self.view_board.count(' ') == 1:
            print(f'Nobody won')
            if not self.start_new_game():
                return False
        return True

    def start_new_game(self):
        while True:
            answer = input('Do you wanna play again? (y or n): ')
            if answer == 'y':
                new_game = True
                break
            elif answer == 'n':
                self.run_menu()
                new_game = False
                break
            else:
                print('AGAIN')
        if new_game:
            print(f"Current score players: {self.player_x_score} : {self.player_0_score}")
            self.drop_board()
            self.run_game()
        else:
            return False

    def run_game(self):
        play = True
        while play:
            if self.player_1 == '':
                self.set_name_players()
            self.choise_marks()
            self.find_mark_x()
            self.find_mark_0()
            self.print_board()
            position_x = self.player_x_turn()
            self.view_board[position_x] = 'X'
            self.print_board()
            play = self.check_winners()
            if play:
                position_0 = self.player_0_turn()
                self.view_board[position_0] = '0'
                self.print_board()
                play = self.check_winners()

    def run_menu(self):
        self.display_main_menu()
        while 1:
            selection = int(input('Enter your choise: '))
            if selection == 1:
                self.run_game()
            elif selection == 2:
                try:
                    self.open_logs()
                    print('')
                except FileNotFoundError:
                    print('Log is empty. You have to start new game')
                finally:
                    self.run_menu()
            elif selection == 3:
                open('logs.txt', 'w').close()
                print('Reset log done')
                self.run_menu()
            elif selection == 4:
                exit()
            else:
                print('Enter 1-4')


if __name__ == "__main__":
    play = Game()
    play.run_menu()
