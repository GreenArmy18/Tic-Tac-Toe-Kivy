from kivy.config import Config
#Config.set('graphics', 'resizable', 0) #disable to change window size, from here: https://stackoverflow.com/questions/37164410/fixed-window-size-for-kivy-programs
Config.set('graphics', 'position', 'custom') #from here: https://stackoverflow.com/questions/43621545/how-to-make-kivy-window-fit-the-screen
Config.set('graphics', 'left', 610)
Config.set('graphics', 'top',  190)
Config.set('graphics', 'borderless', 'True') #from here: https://stackoverflow.com/questions/25639073/how-to-hide-remove-the-default-minimize-maximize-buttons-on-window-developed-wit

#if with border:
#Config.set('graphics', 'left', 610)
#Config.set('graphics', 'top',  205)

#TO-DO List:
#1. class of checking if a button already played and print mesg
#תיעוד לכל המחלקות והפעולות, כולל פלט וקלט ואיזה פרמטרים כל מחלקה ופעולה מקבלת .2

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import (ListProperty, NumericProperty)
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
import random
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
import time
#from kivy.graphics import Color, Rectangle

Window.clearcolor=(0,153/255,102/255,.7)
#Window.clearcolor=(1,1,1,1)
Window.size=(700, 700) #ReSize the window of the game to square



class TicTacToe(GridLayout): #Our main class
    
    status=ListProperty([0,0,0, #the grid of the buttons
                         0,0,0,
                         0,0,0])
    
    current_player=NumericProperty(1) #Our currnet player, starting with 'O'
    
    def __init__(self, *args, **kwargs):
        super(TicTacToe, self).__init__(*args, **kwargs)
        
        self.none1=Label(text="")
        self.title=Label(text="[color=075951]Welcome to my Tic-Tac-Toe game![/color]\n            [color=2040a3]Let's have some FUN[/color] [color=ccac00]:)[/color]", markup=True, font_size=40, bold=True)
        #009999
        #0da192
        self.none2=Label(text="")
        
        '''with self.title.canvas.before:
            Color(0,153/255,102/255,.7)
            #Color(.1 ,.1, .1, 1)
            Rectangle(pos=(0,560), size=(700,140))'''
        
        self.add_widget(self.none1)
        self.add_widget(self.title)
        self.add_widget(self.none2)

        for row in range(3):
            for column in range(3):
                grid_entry=GridEntry(coords=(row,column))
                #font_size=self.height
                grid_entry.bind(on_release=self.button_pressed)
                grid_entry.background_color=(102/255, 102/255, 102/255, .5)
                self.add_widget(grid_entry)
        
        bl1=GridLayout(cols=3)
        bl2=GridLayout(cols=3)
        
        b1=Button(text="[color=#009966]Restart[/color]", font_size=35, size_hint=(1, 1), on_release=self.reset, bold=True, background_color=(0,.4,1,1), markup=True)
        self.scoreboard=Label(text="[color=2040a3]Score Board:[/color]\n[color=000000]  [color=145128]X[/color]: 0 – 0 :[color=102e87]O[/color][/color]\n        [color=000000]D: 0[/color]", font_size=35, bold=True, markup=True)
        #041340
        #7F0000
        #background_window+color= #089c64
        #green: 0F3D1E
        #red: FF0000
        #blue: 3333ff
        
        #self.scoreboard.on_ref_press(self.on_touch_up)
        #with self.scoreboard.canvas:
            #Color(0, 1, 0, 0.25)
            #Rectangle(pos=(.2,1), size=self.scoreboard.size)
            #, background_color=(0,0,0,1)
        b2=Button(text="Exit", font_size=35, size_hint=(1, 1), on_release=self.exit, bold=True, background_color=(0,.4,1,1))
        
        bl1.add_widget(b1)
        bl2.add_widget(b2)
        
        self.add_widget(bl1)
        self.add_widget(self.scoreboard)
        self.add_widget(bl2)
    
    '''def on_touch_up(self, touch):
        self.update()
    
    def update(self):
        self.scoreboard.text="[color=3333ff]Score Board:[/color]\n[color=000000]  [color=33CC66]X[/color]: 0 – 0 :[color=FF0000]O[/color][/color]\n        [color=000000]D: 0[/color]"'''

    def exit(self, obj): #The exit popup and it's buttons
        self.box_popup=BoxLayout(orientation='horizontal')
        #print(self.box_popup.size)
        self.box_popup.add_widget(Label(text="                              Are you sure you want to exit?", font_size=22, pos_hint={'x':0, 'y':.1}))
        
        self.box_popup.add_widget(Button(
            text="Yes",
            on_release=self.bye,
            size_hint=(0.45, 0.2),
            background_color=(1,0,0,1)))

        self.popup_exit=Popup(
            title="Confirmation",
            title_align='justify',
            #separator_color=[40/255, 40/255, 40/255, 1],
            title_size=30,
            content=self.box_popup,
            size_hint=(.5, .4),
            auto_dismiss=True)

        self.box_popup.add_widget(Button(
        text="No",
        on_press=lambda *args: self.popup_exit.dismiss() ,
        size_hint=(0.45, 0.2),
        background_color=(.2,.8,.4,1)))
 
        self.popup_exit.open()

    def bye(self, obj): #closing the app
        #print("The results:", self.scoreboard.text)    
        #print("\nYou chose to exit.\nHave a nice day, Good Bye :)\n")
        #App.get_running_app().stop()
        Bye().myfunc()

    def updateScore(self, winner): #Update the score board
        t=list(self.scoreboard.text)
        #print(t.index('0', 45))
        #print([i for i, x in enumerate(t) if x == "0"])
        
        if winner=="The winner is X!":
            t[76]=str(int(t[76])+1)
            self.scoreboard.text="".join(t)
        elif winner=="The winner is O!":
            t[80]=str(int(t[80])+1)
            self.scoreboard.text="".join(t)
        else:
            t[140]=str(int(t[140])+1)
            self.scoreboard.text="".join(t)
    def button_pressed(self, button): #If the user click on a button
        
        
        
        players={1: 'O', -1: 'X'} #Our players and their signs 
        colours={1: (32/255, 64/255, 163/255,1), -1: (.2,.8,.4,1)} #The colors of each player
        #.2, .1, .73, 1
        #0,1,0,1
        #51,204,102,1
        
        row, column=button.coords
        status_index=3*row+column
        already_played=self.status[status_index]
        
        if not already_played: #If the selected button not already chose
            a=('{} button clicked!'.format(button.coords))
            b=list(a)
            b[1], b[4]=str(int(b[1])+1), str(int(b[4])+1)
            print("".join(b))
            self.status[status_index]=self.current_player
            button.text={1: 'O', -1: 'X'}[self.current_player]
            button.background_color=colours[self.current_player]
            self.current_player*=-1
            
        else:
            a1=("\nThis button {} is already pressed.\n".format(button.coords))
            b1=list(a1)
            b1[14], b1[17]=str(int(b1[14])+1), str(int(b1[17])+1)
            print("".join(b1))
    
    
    
    '''def button_pressed(self, button): #If the user click on a button
        players={1: 'O', -1: 'X'} #Our players and their signs 
        colours={1: (32/255, 64/255, 163/255,1), -1: (.2,.8,.4,1)} #The colors of each player
        #1,0,0,1
        #.2, .1, .73, 1
        #0,1,0,1
        #51,204,102,1
        
        row, column=button.coords
        status_index=3*row+column
        already_played=self.status[status_index]
        
        self.status[status_index]=self.current_player
        button.text={1: 'O', -1: 'X'}[self.current_player]
        button.background_color=colours[self.current_player]
        self.current_player*=-1
        
        if not already_played: #If the selected button not already chose
            a=('{} button clicked!'.format(button.coords))
            b=list(a)
            b[1], b[4]=str(int(b[1])+1), str(int(b[4])+1)
            print("".join(b))
        else:
            print("This button is already pressed.")



        if not already_played: #If the selected button not already chose
            self.status[status_index]=self.current_player
            button.text={1: 'O', -1: 'X'}[self.current_player]
            button.background_color=colours[self.current_player]
            self.current_player*=-1
            
            a=('{} button clicked!'.format(button.coords))
            b=list(a)
            b[1], b[4]=str(int(b[1])+1), str(int(b[4])+1)
            print("".join(b))
        else:
            a1=("\nThis button {} is already pressed.\n".format(button.coords))
            b1=list(a1)
            b1[14], b1[17]=str(int(b1[14])+1), str(int(b1[17])+1)
            print("".join(b1))'''
            
            

    def on_status(self, instance, new_value): #Checing if we have a winner
        status=new_value #Taking the board

        sums=[sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), #Rows
              sum(status[0::3]), sum(status[1::3]), sum(status[2::3]), #Columns
              sum(status[::4]), sum(status[2:-2:2])] #Diagonals

        winner=None
        if 3 in sums:
            winner="The winner is O!"
            print("\n  ",winner,"\n—————————————————————")
        elif -3 in sums:
            winner="The winner is X!"
            print("\n  ",winner,"\n—————————————————————")
        elif 0 not in self.status:
            winner="It's a Draw!"
            print("\n    ",winner,"\n——————————————————————")
        
        if winner: #We have a winner!
            self.updateScore(winner) #Modifies the scoreboard accordingly
            popup=ModalView(size_hint=(0.6, 0.4), pos_hint={'x':.2, 'y':.3})
            #green: background_color=(111/255, 197/255, 168/255, 1)
            #transparent: background_color=(1,1,1,0)
            victory_label=Label(text=winner, font_size=50, bold=True)
            popup.add_widget(victory_label)
            popup.bind(on_dismiss=self.reset)
            popup.open()            
            
            print("\n~~~ New game is starting! ~~~\nClick everywhere outside the popup to clear the board.\n")

    def reset(self, instance): #Reset the board
        
        if self.status==[0 for _ in range(9)]: #Moving over the whole board buttons
            print("The board is already cleared.")
        else:
            self.status=[0 for _ in range(9)]
            for child in self.children:
                if child!=self.scoreboard and child!=self.title:
                    child.text=''
                    child.background_color=(102/255, 102/255, 102/255, .5)
            print("The board has been cleared.\n")
        
        self.current_player=random.choice([1,-1])

class GridEntry(Button): #Class of the coordinations
    coords=ListProperty([0, 0]) #Coordinations of each one of the buttons


class Bye:
  def myfunc(self):
    print("You chose to exit.\nHave a nice day, Good Bye :)\n")
    App.get_running_app().stop()  


class TicTacToeApp(App):
    def build(self):
        self.title="The Ofek's Tic-Tac-Toe game"
        return TicTacToe()

if __name__ == "__main__":
    TicTacToeApp().run()