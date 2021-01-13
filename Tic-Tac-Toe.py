"""
Module main.py
--------------

This is the main module of the program. It contains the definition of the kivy app and configuration functions.
"""
import os

# Import this class to change some things in the kivy window
from kivy.config import Config

# It is necessary that these lines be first, so that they run before everything else
Config.set("graphics", "position", "custom")  # Set a custom position of the window
Config.set("graphics", "left", 610)  # Custom position from left
Config.set("graphics", "top", 190)  # Custom position from the top
Config.set("graphics", "borderless", "1")  # Without a border

import kivy
from kivy.app import App
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    SlideTransition,
    SwapTransition,
)
from kivy.uix.modalview import ModalView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.clock import Clock
from copy import deepcopy
from enum import Enum
from math import inf
from functools import partial
from kivy.lang import Builder
from kivy.core.window import Window

kivy.require("1.11.0")


# TODO: Set up difficulty menu
#       change and redesign the winner popup - V

Builder.load_string(
    """
#: kivy 1.11.0

<Cell@Button>:
    background_color: 102 / 255, 102 / 255, 102 / 255, 0.5
    font_size: 144
    background_normal: ''
    background_down: ''

<MainMenu@Screen>:
    name: 'home'
    canvas:
        Color:
            rgba: 0, 153 / 255, 102 / 255, 0.7
        Rectangle:
            size: root.size
            pos: root.pos
    Label:
        size_hint: None, None
        text: "[color=075951]Welcome to my Tic-Tac-Toe game![/color]\\n\\n           [color=2040a3]Let's have some FUN[/color] [color=b79a00]:)[/color]"
        markup: True
        bold: True
        #color: 0, 0, 0, 1
        font_size: 43
        size: self.texture_size
        pos: ((root.width / 2) - (self.width/ 2)), ((root.height / 2) - (self.height / 2)) + 100

    GridLayout:
        size_hint: None, None
        size: root.width * 0.9, 100
        pos: ((root.width / 2) - (self.width/ 2)), 175
        spacing: 10
        cols: 3
        
        Button:
            text: 'Two Players'
            background_normal: ""
            background_color: 0,61/255,153/255, 1
            font_size: 35
            markup: True
            bold: True
            color: 1, 1, 1, 1
            outline_color: (0, 0, 0)
            outline_width: 4
            on_release: app.root.current = 'mp'
        
        Button:
            text: 'One Player'
            background_normal: ""
            background_color: 0,61/255,153/255, 1
            font_size: 35
            markup: True
            bold: True
            color: 1, 1, 1, 1
            outline_color: (0, 0, 0)
            outline_width: 4
            #color: 0, 153 / 255, 102 / 255, 0.7
            on_release: app.root.current = 'sp'
        
        Button:
            text: 'Exit'
            background_normal: ""
            background_color: 0,61/255,153/255, 1
            font_size: 35
            markup: True
            bold: True
            color: 1, 1, 1, 1
            outline_color: (0, 0, 0)
            outline_width: 4
            on_release: quit()

"""
)


class MainMenu(Screen):
    pass


class PlayMenu(Screen):
    pass


class Player(Enum):
    COMPUTER = "O"
    HUMAN = "X"
    EMPTY = ""


class SimpleBoard:

    MAX_SCORE = 10000

    def __init__(self, board):
        self.__board = [[button.text for button in row] for row in board]

    def __getitem__(self, index):
        return self.__board[index]

    def __len__(self):
        return len(self.__board)

    def __iter__(self):
        return iter(self.__board)

    def is_full(self):
        return not any(
            [symbol == Player.EMPTY.value for row in self.__board for symbol in row]
        )

    def has_won(self):
        return abs(evaluate(self)) == SimpleBoard.MAX_SCORE


def get_possibilities(board, symbol):
    """
    :param board:   The board to insert :symbol: into
    :param symbol:  The symbol to insert into :board:
    :return:        A list of tuples containing:
                    0 - A copy of :board: with :symbol: inserted into an empty spot
                    1 - The indexes (i and j) where :symbol: was inserted
    """
    out = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == Player.EMPTY.value:
                option = deepcopy(board)
                option[i][j] = symbol
                out.append((option, (i, j)))
    return out


def evaluate(board):
    """
    :param board:   The board to evaluate
    :return:        :board:'s score based on the number of 2 in a rows
    """
    lines = check_rows(board) + check_cols(board) + check_diags(board)
    two_in_row = [0, 0]
    for line in lines:
        for i in range(len(line)):
            if line[i] == len(board):
                return SimpleBoard.MAX_SCORE * (-1 if i == 1 else 1)
            if line[i] == len(board) - 1 and line[1 - i] == 0:
                two_in_row[i] += 1
    comp_score = 10 * two_in_row[0]
    player_score = 1.5 * 10 * two_in_row[1]
    return comp_score - player_score


def check_rows(board):
    """
    :param board:   The game board or a list of rows
    :return:        A list containing how many of each symbol is in each row in :board:
    """
    out = []
    for row in board:
        out.append((row.count(Player.COMPUTER.value), row.count(Player.HUMAN.value)))
    return out


def check_cols(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each column in :board:
    """
    transpose = [[row[i] for row in board] for i in range(len(board))]
    return check_rows(transpose)


def check_diags(board):
    """
    :param board:   The game board
    :return:        A list containing how many of each symbol is in each diagonal in :board:
    """
    diagonals = [
        [board[i][i] for i in range(len(board))],
        [board[i][len(board) - i - 1] for i in range(len(board))],
    ]
    return check_rows(diagonals)


def minimax(board, depth):
    """
    :param board:   The current gamestate
    :param depth:   How many moves the function can look ahead
    :return:        The i and j indexes of the best move
    """
    alpha = -inf
    beta = inf
    if depth <= 0:
        return pick_highest(board)
    return make_move(board, Player.COMPUTER, alpha, beta, depth, depth)


def pick_highest(board):
    """
    :param board:   The current gamestate
    :return:        The move with the highest rating
    """
    options = get_possibilities(board, Player.COMPUTER.value)
    scores = [evaluate(x[0]) for x in options]
    return options[scores.index(max(scores))][1]


def make_move(board, player, alpha, beta, depth, idepth):
    """
    :param board:   A simplified version of the current board
    :param player:  The player the algorithm is playing as (Can only be an instance of Player)
                    (Note: the function maximises for the computer and minimises for the player)
    :param alpha:   Lower bound for best_score
    :param beta:    Upper bound for best_score
    :param depth:   How many moves the algorithm can look ahead
    :param idepth:  The initial depth
    :return:        The best score or the index of the best move for :player:
    """
    val = evaluate(board)
    if abs(val) == SimpleBoard.MAX_SCORE:
        return val * (depth + 1)
    if depth == 0 or board.is_full():
        return val
    options = get_possibilities(board, player.value)
    n_player = Player.COMPUTER if player == Player.HUMAN else player.HUMAN
    best_index = options[0][1]
    best_score = make_move(options[0][0], n_player, alpha, beta, depth - 1, idepth)
    for option in options[1:]:
        score = make_move(option[0], n_player, alpha, beta, depth - 1, idepth)
        if better_move(player, score, best_score):
            best_index = option[1]
            best_score = score
        if alpha < best_score and player == Player.COMPUTER:
            alpha = best_score
        elif beta > best_score and player == Player.HUMAN:
            beta = best_score
        if beta <= alpha:
            break
    return best_score if depth != idepth else best_index


def better_move(player, score, best_score):
    """
    :param player:      Tells the computer if looking for min or max scores (str, Player.HUMAN/Player.COMPUTER)
    :param score:       The new score
    :param best_score:  The previous best score
    :return:            If :score: is better than :best_score:
    """
    return score > best_score if player == Player.COMPUTER else score < best_score


class GameMode(Enum):
    SINGLE_PLAYER = 0
    MULTI_PLAYER = 1


class Color(Enum):
    O = (32 / 255, 64 / 255, 163 / 255, 1)  # The color for the O's buttons
    X = (0.2, 0.8, 0.4, 1)  # The color for the X's buttons

    # In Single Player Mode:
    # COMPUTER = "O"
    # HUMAN = "X"


X, D, O = 0, 0, 0  # global variables for the scores


class Board(GridLayout):
    LENGTH = 3
    # Default difficult level is "hard"
    DIFFICULTY = {
        "baby": 0,
        "easy": 2,
        "medium": 4,
        "hard": 6,
        "impossible": LENGTH ** 2,
    }

    def __init__(self, **kwargs):
        super().__init__()

        self.cols = self.rows = Board.LENGTH
        self.spacing = 2, 2
        self.click_sound = SoundLoader.load(os.path.join("assets", "click.wav"))
        self.game_start = SoundLoader.load(os.path.join("assets", "app_start.wav"))
        self.new_game_starting = SoundLoader.load(os.path.join("assets", "start.wav"))
        self.win_game = SoundLoader.load(os.path.join("assets", "win.mp3"))
        self.lose_game = SoundLoader.load(os.path.join("assets", "lose.wav"))

        self.first_player = self.current_player = kwargs.get(
            "first_player", Player.HUMAN
        )
        self.game_mode = kwargs.get("game_mode", GameMode.SINGLE_PLAYER)
        self.depth = Board.DIFFICULTY[kwargs.get("difficulty")]
        self.button_list = [
            [Cell() for _ in range(Board.LENGTH)] for _ in range(Board.LENGTH)
        ]
        self.popup = None
        if self.game_start:
            self.game_start.play()
        self.init_buttons()
        self.first_move()

    def init_buttons(self, reset=False):
        """
        Initialises/resets the button objects in self.button_list by doing the following:
        - Binding the on_click function
        - Setting the buttons text value to a blank string  (On reset)
        - Adding the button to the Board                    (On init)

        Also, create the reset widgets in the board - the 3 button in bottom - Reset, Back and Exit and the ScoreBoard in top
        :param reset:   Whether to reset or initialise the buttons
        :return:        None
        """

        if self.new_game_starting:  # If the sound of new game is exist
            self.new_game_starting.play()  # So, play it

        board = BoxLayout(orientation="vertical")
        grid = GridLayout(cols=3, rows=3, spacing=2)
        for row in self.button_list:
            for button in row:
                button.bind(on_release=self.on_click)
                if reset:
                    button.text = ""
                    button.background_color = 102 / 255, 102 / 255, 102 / 255, 0.5
                else:
                    grid.add_widget(button)

        grid.pos_hint = {"x": 0.003, "y": 0}

        if not reset:
            self.restart = Button(
                text="[color=#009966]Restart[/color]",
                font_size=35,
                size_hint=(1, 1),
                on_release=self.reset,
                bold=True,
                background_color=(0, 0.4, 1, 1),
                markup=True,
            )

            # Creating the score board text label and design it
            self.scoreboard = Label(
                text="[color=2040a3]Score Board:[/color]\n[color=000000]  [color=145128]X[/color]: 0 – 0 :[color=102e87]O[/color][/color]\n        [color=000000]D: 0[/color]",
                font_size=35,
                bold=True,
                markup=True,
            )

            # Creating the exit button and design it. also, call in realse click on the button to the exit function
            self.exit = Button(
                text="[color=#009966]Exit[/color]",
                font_size=35,
                size_hint=(1, 1),
                on_release=self.exitPopup,
                bold=True,
                background_color=(0, 0.4, 1, 1),
                markup=True,
            )

            self.back = Button(
                text="[color=#009966]Back[/color]",
                font_size=35,
                size_hint=(1, 1),
                on_release=lambda *args: self.goto_menu(),
                bold=True,
                background_color=(0, 0.4, 1, 1),
                markup=True,
            )

            buttons = BoxLayout(orientation="horizontal", padding=[0, 2, 0, 0])

            buttons.add_widget(self.restart)  # Add the reset widget to the board
            buttons.add_widget(self.back)
            buttons.add_widget(self.exit)  # Add the exir widget to the board

            buttons.size_hint = (1.003, 0.3)
            buttons.pos_hint = {"x": 0.001}

            self.scoreboard.pos_hint = {"top": 0.8}
            self.scoreboard.size_hint = (1, 0.4)

            board.add_widget(self.scoreboard)  # Add the score board widget to the board

            board.add_widget(grid)
            board.add_widget(buttons)
            self.add_widget(board)

    def exitPopup(self, obj):  # The exit popup and its buttons
        self.box_popup = BoxLayout(
            orientation="horizontal"
        )  # Create a box layout fot the exit popup

        self.popup_exit = Popup(
            title="Confirmation",
            title_align="justify",
            title_size=30,
            content=self.box_popup,
            size_hint=(0.5, 0.4),
            auto_dismiss=True,
        )

        # Add for it text and design and reposition it
        self.box_popup.add_widget(
            Label(
                text="                               Are you sure you want to exit?",
                font_size=22,
                pos_hint={"x": 0, "y": 0.1},
            )
        )

        self.box_popup.add_widget(
            Button(
                text="Yes",
                on_release=self.bye,
                size_hint=(0.45, 0.2),
                background_color=(1, 0, 0, 1),
            )
        )

        self.box_popup.add_widget(
            Button(
                text="No",
                on_press=lambda *args: self.popup_exit.dismiss(),
                size_hint=(0.45, 0.2),
                background_color=(0.2, 0.8, 0.4, 1),
            )
        )

        self.popup_exit.open()

    def bye(self, obj):  # Function for closing the app
        # Calling the closing function with the score board text
        Bye().myfunc(self.scoreboard.text)
        self.popup_exit.dismiss()  # Do not forget to close the currnet popup ;)
        self.reset_all(obj)  # Clear the board

    def updateScore(self, winner):  # Update the score board
        # The initial score board text
        ScoreBoardText = "[color=2040a3]Score Board:[/color]\n[color=000000]  [color=145128]X[/color]: {} – {} :[color=102e87]O[/color][/color]\n        [color=000000]D: {}[/color]"
        global X, O, D  # Our global variables: X, O and D (for draws)
        # print(self.scoreboard.text)
        if winner == "The Winner is X!":  # If the winner is X
            X += 1  # Add 1 to the X's score
        elif winner == "The winner is O!":  # If the winner is O
            O += 1  # Add 1 to the O's score
        else:
            # If the winner isn't X or O, it's probably a draw
            if winner == "It's a Draw!":
                D += 1  # Add 1 to the draws score
        # Upadating the score board text by replacing the {} signs with the new scores
        self.scoreboard.text = ScoreBoardText.format(X, O, D)

    def first_move(self):
        """
        Runs the first move if the first player is a computer
        :return:    None
        """
        if (
            self.game_mode == GameMode.SINGLE_PLAYER
            and self.first_player == Player.COMPUTER
        ):
            self.computer_move()

    def on_click(self, touch):
        """
        Runs the code for the player's turn
        :param touch:   The button that was pressed
        :return:        None
        """
        if self.click_sound:
            self.click_sound.play()
        game_over = self.insert(touch, self.current_player.value)
        self.set_current_player()
        if not game_over and self.game_mode == GameMode.SINGLE_PLAYER:
            self.computer_move()

    def computer_move(self):
        """
        Makes the computer's move (Single-player only)
        :return:        None
        """
        i, j = minimax(SimpleBoard(self.button_list), self.depth)
        self.insert(self.button_list[i][j], self.current_player.value)
        self.set_current_player()

    def set_current_player(self):
        """
        Sets the current player
        :return:        None
        """
        self.current_player = (
            Player.COMPUTER if self.current_player != Player.COMPUTER else Player.HUMAN
        )

    def insert(self, button, symbol):
        """
        Places :symbol: on :button: and then checks if the game has ended
        :param button:  The button to place :symbol: on
        :param symbol:  The :symbol: to place
        :return:        If the game has ended
        """

        button.text = symbol
        button.background_color = (
            Color.O.value if symbol == Player.COMPUTER.value else Color.X.value
        )
        button.unbind(on_release=self.on_click)
        board = SimpleBoard(self.button_list)

        has_won = board.has_won()
        is_full = board.is_full()
        self.title = "It's a Draw!" if is_full else None
        if symbol == "X":
            self.title = "The Winner is X!" if has_won else self.title
            if self.game_mode == GameMode.SINGLE_PLAYER and has_won:
                if self.win_game:
                    self.win_game.play()
        if symbol == "O":
            self.title = "The winner is O!" if has_won else self.title
            if self.game_mode == GameMode.SINGLE_PLAYER and has_won:
                if self.lose_game:
                    self.lose_game.play()

        if self.title is not None:
            # Print a message accordingly
            print("\n  ", self.title, "\n—————————————————————")
            self.end_message(self.title)
            self.updateScore(self.title)

        return has_won or is_full

    def end_message(self, message):
        """
        Displays an end message and asks user to start a new game or exit
        :param message: The message to display
        :return:        None
        """
        self.disabled = True
        Clock.schedule_once(self.popup_contents, 2)

    def popup_contents(self, button):
        """
        Generates the contents for the end of game popup
        :return:    The popup's contents
        """

        message = self.title
        # Create a modal view popup and reposition and resize it
        self.popup = ModalView(
            size_hint=(0.4, 0.2),
            background_color=(0, 153 / 255, 102 / 255, 0.7),
            background="atlas://data/images/defaulttheme/action_item",
        )

        # Create and design the text labals, in a box layout
        victory_label = BoxLayout(orientation="vertical")
        # Add the first text label, with the winner
        victory_label.add_widget(
            Label(
                text=message,
                font_size=50,
                bold=True,
                markup=True,
            )
        )
        # Add the second text label, with a message
        victory_label.add_widget(
            Label(
                text="Click everywhere in the screen to clear the board",
                font_size=25,
                markup=True,
                pos_hint={"x": 0, "y": -0.55},
                outline_color=(0, 0, 0),
                outline_width=1,
                color=(1, 1, 1),
            )
        )

        self.popup.add_widget(victory_label)  # Add the labal to the popup

        # When the player click outside the popup, it dismiss. then, call the "reset" function to clear the board
        self.popup.bind(on_dismiss=self.reset)
        # Or, wait 2 seconds to auto dismiss
        Clock.schedule_once(self.dismiss_popup, 2)
        self.popup.open()  # Open the popup
        # The board has been cleard and a new game is starting, so printing a message accordingly
        print(
            "\n~~~ New game is starting! ~~~\nClick everywhere in the screen to clear the board.\n"
        )

    def dismiss_popup(self, dt):  # function to dismiss the popup
        if self.popup:
            self.popup.dismiss()  # Dismiss the popup

    def goto_menu(self):
        """
        Resets the game and goes to the main menu
        :return:    None
        """

        sm = self.parent.parent.manager
        sm.transition.direction = "right"
        self.reset_all(self)
        sm.current = "menu"

    def reset(self, button):
        """
        Resets the game, called from end of game popup
        :return:    None
        """
        self.disabled = False
        self.init_buttons(reset=True)
        self.first_player = (
            Player.COMPUTER if self.first_player != Player.COMPUTER else Player.HUMAN
        )
        self.current_player = self.first_player
        self.first_move()

    def reset_all(self, button):
        """
        Resets the game, called from end of game popup
        :return:    None
        """
        self.scoreboard.text = "[color=2040a3]Score Board:[/color]\n[color=000000]  [color=145128]X[/color]: 0 – 0 :[color=102e87]O[/color][/color]\n        [color=000000]D: 0[/color]"
        global X, O, D
        X, O, D = 0, 0, 0

        if self.popup is not None:
            self.popup.dismiss()
            self.popup = None
        self.disabled = False
        self.init_buttons(reset=True)
        self.first_player = (
            Player.COMPUTER if self.first_player != Player.COMPUTER else Player.HUMAN
        )
        self.current_player = self.first_player
        self.first_move()


class Cell(Button):
    pass


class Bye:
    # Exit the game and print Its results and the actual winner of all games
    def myfunc(self, text):
        # Print a message accordingly
        print("You chose to exit.\n\n  ~~~ GAME OVER ~~~\n——————————————————————")
        # Getting the positions of any sign from the score board text
        Xpos, Opos, Dpos = (
            text[76],
            text[80],
            text[140],
        )
        winner = text
        if Xpos > Opos:
            if Xpos == "1":
                winner = "The winner in all games is X,\nwith ONE win!\n"
                print(winner)  # Print a message accordingly
            else:
                winner = "The winner in all games is X,\nwith " + str(Xpos) + " wins!\n"
                print(winner)  # Print a message accordingly
        elif Xpos < Opos:
            if Opos == "1":
                winner = "The winner in all games is O,\nwith ONE win!\n"
                print(winner)  # Print a message accordingly
            else:
                winner = "The winner in all games is O,\nwith " + str(Opos) + " wins!\n"
                print(winner)  # Print a message accordingly
        else:
            if Dpos > "0" or (Dpos == "0" and Xpos > "0" and Opos > "0"):
                winner = "We have no winner,\nthe game ended in a draw!\n"
                print(winner)  # Print a message accordingly
            else:
                winner = "You have not played any game,\nso we have no winner.\n\nThe game ended in a draw!\n"
                print(winner)  # Print a message accordingly


        self.popup = ModalView(
            size_hint=(0.8, 0.4),
            background_color=(0 / 255, 97 / 255, 97 / 255, 1),
            auto_dismiss=False,
        )

        # Create and design the text labals, in a box layout
        victory_label = BoxLayout(orientation="horizontal")

        # Add the first text label, with the winner
        self.sum_games = Label(
            text=winner,
            font_size=37,
            bold=True,
            markup=True,
            pos_hint={"x": 0, "y": -0.05},
            halign="center",
            color=(0 / 255, 97 / 255, 97 / 255, 1),
        )
        victory_label.add_widget(self.sum_games)

        self.popup.add_widget(victory_label)  # Add the labal to the popup
        self.popup.open()  # Open the popup

        # Schedule the change the label's text by 3.5 seconds
        Clock.schedule_once(partial(Bye.text_change, self), 3.5)

    def text_change(self, obj):
        self.sum_games.text = "Have a nice day,\nGood Bye :)"
        self.sum_games.font_size = 70
        self.sum_games.pos_hint = {"x": 0, "y": 0}
        self.sum_games.outline_width = 0

        print("Have a nice day, Good Bye :)\n")  # Print a message accordingly

        # Schedule the closing of the app by 2.5 seconds
        Clock.schedule_once(partial(self.close), 2.5)

    def close(self, obj):
        App.get_running_app().stop()  # Stoping the app, GOOD BYE!


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(name=kwargs["name"])
        board = BoxLayout(orientation="vertical")

        self.grid = Board(
            game_mode=kwargs.get("game_mode", GameMode.SINGLE_PLAYER),
            first_player=kwargs.get("first_player", Player.HUMAN),
            difficulty=kwargs.get("difficulty", "hard"),
        )

        board.add_widget(self.grid)
        self.add_widget(board)


class TicTacToeApp(App):

    __sm = None

    def config_setup(self):
        """
        Configures the program
        :return:    None
        """
        path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(path)
        self.title = "Ofek's Tic-Tac-Toe"
        self.icon = os.path.join("assets", "icon.png")
        Window.clearcolor = (0, 153 / 255, 102 / 255, 0.7)  # My background new color
        Window.size = (700, 700)  # Resize the window of the game to a square shape

    @staticmethod
    def get_sm():
        """
        Generates the screen manager if it is None and returns it
        :return:    The program's ScreenManager
        """

        if TicTacToeApp.__sm is None:
            TicTacToeApp.__sm = ScreenManager(transition=SwapTransition())
            TicTacToeApp.__sm.add_widget(MainMenu(name="menu"))
            TicTacToeApp.__sm.add_widget(
                GameScreen(name="sp", game_mode=GameMode.SINGLE_PLAYER)
            )
            TicTacToeApp.__sm.add_widget(
                GameScreen(name="mp", game_mode=GameMode.MULTI_PLAYER)
            )
        else:
            print("hi")
        return TicTacToeApp.__sm

    def build(self):
        self.config_setup()
        return TicTacToeApp.get_sm()


if __name__ == "__main__":
    TicTacToeApp().run()
