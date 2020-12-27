# Creator: Ofek Cohen
# Kivy version used: 1.11.1
# Python version used: 3.7.8

# Import this class to change some things in the kivy window
from kivy.config import Config

# It is necessary that these lines be first, so that they run before everything else
Config.set("graphics", "position", "custom")  # Set a custom position of the window
Config.set("graphics", "left", 610)  # Custom position from left
Config.set("graphics", "top", 190)  # Custom position from the top
Config.set("graphics", "borderless", "1")  # Without a border

from kivy.app import App
from kivy.uix.gridlayout import GridLayout  # Import the grid layout to the buttons grid
from kivy.uix.button import Button  # Import the button's class
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

# Specifies the default value of the property. in our case - the default grid list of the buttons
from kivy.properties import ListProperty

# Specifies the default value of the property. in our case - the default player sign
from kivy.properties import NumericProperty

# Import this class to "load" .kv file without creating the file
from kivy.lang.builder import Builder

# Import this class to schedule the dismiss of the popup's winner
from kivy.clock import Clock

# Import this class to change the settings of the kivy's window game
from kivy.core.window import Window

Window.clearcolor = (0, 153 / 255, 102 / 255, 0.7)  # My background new color
Window.size = (700, 700)  # Resize the window of the game to a square shape

# The string of the .kv file, without it
# I using the builder package to do it
Builder.load_string(
    """
<TicTacToe>:
	cols: 3         # The number of columns of the grid
    
<GridEntry>:
	font_size: self.height      # Set the font size of players to the size of any button

"""
)

X, D, O = 0, 0, 0  # global variables for the scores


class TicTacToe(GridLayout):  # Our main class
    # Our default grid of the buttons
    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])

    players = {1: "O", -1: "X"}  # The players and their signs
    # Our currnet player, default and starting with 'O' - 1
    current_player = NumericProperty(1)

    def __init__(self, *args, **kwargs):  # My main function
        super(TicTacToe, self).__init__(*args, **kwargs)  # Create the super function

        self.none1 = Label(text="")  # Empty label for space

        # The title of my game, with some cosmetic changes
        self.title = Label(
            text="[color=075951]Welcome to my Tic-Tac-Toe game![/color]\n            [color=2040a3]Let's have some FUN[/color] [color=b79a00]:)[/color]",
            markup=True,
            font_size=40,
            bold=True,
        )

        self.none2 = Label(text="")  # Another empty label for space

        self.add_widget(self.none1)  # Add the first empty label to the self widget
        self.add_widget(self.title)  # Add the title labal to the self widget
        self.add_widget(self.none2)  # Add the second empty label to the self widget

        # Creating the game board
        for row in range(3):  # Starting with the rows
            for column in range(3):  # And now the columns
                # create a grid entry by the coordinates of the rows and columns, using the class "GridEntry"
                grid_entry = GridEntry(coords=(row, column))
                # Enter the buttons of each one to the grid and make call, when release them, to the function "button_pressed"
                grid_entry.bind(on_release=self.button_pressed)
                # change the color of the button
                grid_entry.background_color = (102 / 255, 102 / 255, 102 / 255, 0.5)
                # Add the grid (with all the buttons) to the self widget
                self.add_widget(grid_entry)

        # Creating the reset button and design it
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

        self.add_widget(self.restart)  # Add the reset widget to the board
        self.add_widget(self.scoreboard)  # Add the score board widget to the board
        self.add_widget(self.exit)  # Add the exir widget to the board

    def exitPopup(self, obj):  # The exit popup and its buttons
        # Create a box layout fot the exit popup
        self.box_popup = BoxLayout(orientation="horizontal")

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

    def updateScore(self, winner):  # Update the score board
        # The initial score board text
        ScoreBoardText = "[color=2040a3]Score Board:[/color]\n[color=000000]  [color=145128]X[/color]: {} – {} :[color=102e87]O[/color][/color]\n        [color=000000]D: {}[/color]"
        global X, O, D  # Our global variables: X, O and D (for draws)

        if winner == "The winner is X!":  # If the winner is X
            X += 1  # Add 1 to the X's score
        elif winner == "The winner is O!":  # If the winner is O
            O += 1  # Add 1 to the O's score
        else:  # If the winner isn't X or O, it's probably a draw
            D += 1  # Add 1 to the draws score

        # Upadating the score board text by replacing the {} signs with the new scores
        self.scoreboard.text = ScoreBoardText.format(X, O, D)

    def button_pressed(self, button):  # If the user click on a button
        players = {1: "O", -1: "X"}  # Our players and their signs
        # The colors of each player
        colours = {
            1: (32 / 255, 64 / 255, 163 / 255, 1),  # The color for the O's buttons
            -1: (0.2, 0.8, 0.4, 1),  # The color for the X's buttons
        }

        row, column = button.coords  # Getting the row and column by the coordinations
        # Multiply by 3 to get the index of the row and column in the grid
        status_index = 3 * row + column
        # Getting the status of the button that has been selected
        already_played = self.status[status_index]

        if not already_played:  # If the selected button not already chose
            # Print a message accordingly when a button has been clicked
            buttonText = "{} button clicked!".format(button.coords)
            # Make it a list to make it easier to work with and modify
            LText = list(buttonText)
            # Add 1 the two variables accordingly, for a better visual display
            LText[1], LText[4] = str(int(LText[1]) + 1), str(int(LText[4]) + 1)
            print("".join(LText))  # Print the result

            self.status[status_index] = self.current_player  # Enter the move
            # change the text of the button accordingly
            button.text = {1: "O", -1: "X"}[self.current_player]
            # change the background color of the button accordingly
            button.background_color = colours[self.current_player]
            self.current_player *= -1  # switch the player sign

        else:  # When the button is already pressed

            # Print a message accordingly
            buttonText = "\nThis button {} is already pressed.".format(button.coords)
            # Make it a list to make it easier to work with and modify
            LText = list(buttonText)
            # Add 1 the two variables accordingly, for a better visual display
            LText[14], LText[17] = str(int(LText[14]) + 1), str(int(LText[17]) + 1)
            print("".join(LText))  # Print the result

    def on_status(self, instance, new_value):  # Checing if we have a winner
        status = new_value  # Taking the board

        # Suming the signs in every way in the board, to find the winner
        sums = [
            sum(status[0:3]),  # Row #1
            sum(status[3:6]),  # Row #2
            sum(status[6:9]),  # Row #3
            sum(status[0::3]),  # column #1
            sum(status[1::3]),  # column #2
            sum(status[2::3]),  # column #3
            sum(status[::4]),  # Diagonal #1 - left to right
            sum(status[2:-2:2]),  # Diagonal #2 - right to left
        ]

        winner = None  # Reset the winner string
        if 3 in sums:  # If we have 3 in one of the places in the list 'sums'
            winner = "The winner is O!"  # So, the winner is O
            # Print a message accordingly
            print("\n  ", winner, "\n—————————————————————")
        elif -3 in sums:  # If we have -3 in one of the places in the list 'sums'
            winner = "The winner is X!"  # So, the winner is O
            # Print a message accordingly
            print("\n  ", winner, "\n—————————————————————")
        # If the board is fully and we still no have a winner
        elif 0 not in self.status:
            winner = "It's a Draw!"  # So, it's a draw
            # Print a message accordingly
            print("\n    ", winner, "\n——————————————————————")

        if winner:  # We have a winner!
            self.updateScore(winner)  # Modifies the scoreboard accordingly
            # Create a modal view popup and reposition and resize it
            self.popup = ModalView(
                size_hint=(0.6, 0.4),
                pos_hint={"x": 0.2, "y": 0.3},
                background_color=(0, 153 / 255, 102 / 255, 0.7),
                background="atlas://data/images/defaulttheme/action_item",
            )
            # filechooser_selected -לבן חצי שקוף
            # action_item - שקוף לגמרי! action_view
            # overflow
            # bubble - חצי שחור
            # spinner_disabled
            # checkbox_disabled_off
            # textinput_active - לבן
            # checkbox_radio_on - תכלת button_pressed
            # checkbox_radio_disabled_off
            # switch-button - אפור בהיר
            # tab_disabled
            # checkbox_off
            # vkeyboard_background - שחור ועגלגל
            # action_group_disabled - כמעט שקוף לגמרי checkbox_radio_off
            # checkbox_radio_disabled_on
            # sliderh_background_disabled - שקוף גרדיאנט
            # tab_btn_disabled_pressed - שקוף, button_disabled
            # switch-button_disabled - חצי שקוף
            # spinner
            # player-background
            # tab_btn_disabled

            # Create and design the text labals, in a box layout
            victory_label = BoxLayout(orientation="horizontal")
            # Add the first text label, with the winner
            victory_label.add_widget(
                Label(
                    text="                  " + winner,
                    font_size=50,
                    bold=True,
                    markup=True,
                )
            )
            # Add the second text label, with a message
            victory_label.add_widget(
                Label(
                    text="Click everywhere outside the popup to clear the board                                           ",
                    font_size=20,
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
                "\n~~~ New game is starting! ~~~\nClick everywhere outside the popup to clear the board.\n"
            )

    def dismiss_popup(self, dt):  # function to dismiss the popup
        self.popup.dismiss()  # Dismiss the popup

    def reset(self, instance):  # Reset the board
        # Moving over the whole board buttons
        # If the whole board is already empty (==0)
        if self.status == [0 for _ in range(9)]:
            print("The board is already cleared.")  # Print a message accordingly
        else:
            # Moving over the board again and make any button to equal to 0 (the default)
            self.status = [0 for _ in range(9)]
            for child in self.children:  # Moving over every button in the grid
                if (  # checking if the currnet position (child) isn't vital
                    child != self.scoreboard  # Not include the score board
                    and child != self.title  # Not include the title
                    and child != self.restart  # Not include the reset button
                    and child != self.exit  # Not include the exit button
                ):
                    child.text = ""  # Reset the text in the button to an empty one
                    # Reset the background color of the button to the default
                    child.background_color = (102 / 255, 102 / 255, 102 / 255, 0.5)
            print("The board has been cleared.\n")  # Print a message accordingly

        self.current_player *= -1  # Switch the player sign


class GridEntry(Button):  # Class of the coordinations
    coords = ListProperty([0, 0])  # Coordinations of each one of the buttons


class Bye(TicTacToe):
    # Exit the game and print Its results and the actual winner of all games
    def myfunc(self, text):
        # Print a message accordingly
        print("You chose to exit.\n\n  ~~~ GAME OVER ~~~\n——————————————————————")
        # Getting the positions of any sign from the score board text
        Xpos, Opos, Dpos = (text[76], text[80], text[140])

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
            if Dpos > "0":
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
        Clock.schedule_once(self.text_change, 3.5)

    def text_change(self, obj):
        self.sum_games.text = "Have a nice day,\nGood Bye :)"
        self.sum_games.font_size = 70
        self.sum_games.pos_hint = {"x": 0, "y": 0}
        self.sum_games.outline_width = 0

        print("Have a nice day, Good Bye :)\n")  # Print a message accordingly

        # Schedule the closing of the app by 2.5 seconds
        Clock.schedule_once(self.close, 2.5)

    def close(self, obj):
        App.get_running_app().stop()  # Stoping the app, GOOD BYE!


class TicTacToeApp(App):  # Building my game
    def build(self):
        self.icon = "tic-tac-toe.png"  # Got a new icon
        self.title = "The Ofek's Tic-Tac-Toe game"  # Get a new title
        return TicTacToe()


if __name__ == "__main__":
    TicTacToeApp().run()  # Run our game!
