from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from functools import partial

from random import choice

from constants import BOLD_LABEL_TEXT, LABEL_TEXT, COLOR_POS_MAP, Clicker, Colors
from simon_button import SimonButton


class SimonApp(App):
    def on_window_resize(self, window, width, height):
        """
        Adjust font sizes when the size of the window changes
        """
        self.game_name.font_size = width // 16
        self.score_label.font_size = width // 50
        self.turn.font_size = width // 50

    def restart_game(self, instance):
        """
        Resetting variables when the game is restarted
        """
        self.game_over_popup.dismiss()
        self.round_num = 1
        self.score = 0
        self.score_label.text = LABEL_TEXT.format(f"Score: {self.score}")
        self.turn.text = LABEL_TEXT.format(str(Clicker.SIMON))
        self.start_round()

    def check_player_seq(self, color):
        """
        Determine whether the player has made the correct choice
        """
        self.player_sequence_lst.append(color)
        cur_index = len(self.player_sequence_lst) - 1
        if self.simon_sequence_lst[cur_index] != color:
            # lose
            self.color_button_map[color].new_round = False
            self.color_button_map[color].game_over = True
        elif len(self.simon_sequence_lst) == len(self.player_sequence_lst):
            # new round
            self.round_num += 1
            self.score += 1
            self.score_label.text = LABEL_TEXT.format(f"Score: {self.score}")
            self.color_button_map[color].new_round = True
            self.color_button_map[color].game_over = False
            self.turn.text = LABEL_TEXT.format(str(Clicker.SIMON))
        else:
            # continue with current round
            self.color_button_map[color].new_round = False
            self.color_button_map[color].game_over = False

    def on_trigger_action(self):
        """
        Schedule an event to light up each button for Simon's turn

        This method of repeatedly calling the same function was used instead of a for loop to ensure
        that the buttons will appear to light up one at a time instead of all once.

        Using sleep does not work as it will delay the main thread and all kivy events run on the main thread.
        After sleep is completed, only the leftover buttons will be triggered all at once.
        """
        # Simon has not finished pressing all his buttons, trigger the next button press
        if self.triggered_button_num < self.round_num - 1:
            self.triggered_button_num += 1
            Clock.schedule_once(
                partial(
                    self.simon_button_trigger,
                    color=self.simon_sequence_lst[self.triggered_button_num],
                ),
                0.7,
            )

    def simon_button_trigger(self, dt, color):
        """
        Callback function for triggering buttons during Simon's turn
        """
        self.color_button_map[color].on_simon_press()

        # after the last Simon button is triggered, there will be 2 events left that are scheduled by Clock
        # use that as the condition to switch turn from Simon to the player
        if (
            len(Clock.get_events()) == 2
            and self.triggered_button_num == self.round_num - 1
        ):
            for color, button in self.color_button_map.items():
                button.clicker = Clicker.PLAYER
            self.turn.text = LABEL_TEXT.format(str(Clicker.PLAYER))

    def simon_sequence(self, instance):
        """
        Event handler for when "Go" button is clicked in the new round popup
        """
        self.start_round_popup.dismiss()

        # update clicker attribute in SimonButton to indicate that it is Simon's turn
        for color, button in self.color_button_map.items():
            button.clicker = Clicker.SIMON

        # Simon picking his color sequence
        for _ in range(self.round_num):
            color = choice(Colors.list())
            self.simon_sequence_lst.append(color)

        # schedule the triggering of the first button here so that on_simon_press handler in SimonButton will
        # be run and on_trigger_action will be called to schedule all the other button trigger events
        self.triggered_button_num = 0
        Clock.schedule_once(
            partial(
                self.simon_button_trigger,
                color=self.simon_sequence_lst[self.triggered_button_num],
            ),
            0.7,
        )

    def game_over(self):
        """
        Create game over pop up
        """
        # create game over popup content layout
        self.game_over_popup_content = GridLayout(cols=1)

        # create game over text
        self.game_over_text = Label(
            text=BOLD_LABEL_TEXT.format("Game Over"),
            markup=True,
            font_size=Window.width // 16,
        )
        self.game_over_popup_content.add_widget(self.game_over_text)

        # create restart button
        self.restart_game_button = Button(
            text="Restart Game",
            font_size=Window.width // 20,
            on_press=self.restart_game,
            background_normal="",
            size_hint=(0.5, 0.5),
        )
        self.restart_game_button.background_color = 232 / 255, 115 / 255, 42 / 255, 1
        self.game_over_popup_content.add_widget(self.restart_game_button)

        # create actual game over popup
        self.game_over_popup = Popup(
            content=self.game_over_popup_content,
            size_hint=(0.5, 0.5),
            separator_height=0,
            background="",
            auto_dismiss=False,
        )
        self.game_over_popup.open()

    def start_round(self):
        """
        Create start of round pop up
        """
        self.simon_sequence_lst = []
        self.player_sequence_lst = []

        # create start of round pop up content layout
        self.start_round_popup_content = GridLayout(cols=1)

        # create round number title
        self.round_popup_title = Label(
            text=BOLD_LABEL_TEXT.format(f"Round {self.round_num}"),
            markup=True,
            font_size=Window.width // 16,
        )
        self.start_round_popup_content.add_widget(self.round_popup_title)

        # create go button
        self.go_button = Button(
            text="Go",
            font_size=Window.width // 20,
            on_press=self.simon_sequence,
            background_normal="",
            size_hint=(0.5, 0.5),
        )
        self.go_button.background_color = 53 / 255, 212 / 255, 209 / 255, 1
        self.start_round_popup_content.add_widget(self.go_button)

        # create actual start of round pop up with content as the layout created above
        self.start_round_popup = Popup(
            content=self.start_round_popup_content,
            size_hint=(0.5, 0.5),
            separator_height=0,
            background="",
            auto_dismiss=False,
        )
        self.start_round_popup.open()

    def on_start(self):
        """
        Set variables when the application starts
        """
        self.round_num = 1
        self.score = 0

        # passing essential SimonApp methods to SimonButton class to be used in on_press
        for _, button in self.color_button_map.items():
            button.on_trigger_action = self.on_trigger_action
            button.check_player_seq = self.check_player_seq
            button.start_round = self.start_round
            button.game_over_func = self.game_over

        # begin first round
        self.start_round()

    def build(self):
        """
        Create elements to be displayed on the application
        """
        self.screen = BoxLayout(orientation="vertical")

        # create top bar
        self.top_bar = FloatLayout(size_hint_y=0.2)
        self.screen.add_widget(self.top_bar)

        # create "Simon Says/Player Says" label
        self.turn = Label(
            text=LABEL_TEXT.format(str(Clicker.SIMON)),
            font_size=Window.width // 50,
            markup=True,
            pos_hint={"x": 0.15, "y": 0},
            size_hint=(None, None),
        )
        self.top_bar.add_widget(self.turn)

        # create game name label
        self.game_name = Label(
            text=BOLD_LABEL_TEXT.format("SIMON"),
            markup=True,
            font_size=Window.width // 16,
            pos_hint={"x": 0.44, "y": 0},
            size_hint=(None, None),
        )
        self.game_name.background_color = 0, 0, 0, 0
        self.top_bar.add_widget(self.game_name)

        # create score label
        self.score_label = Label(
            text=LABEL_TEXT.format("Score: 0"),
            font_size=Window.width // 50,
            markup=True,
            pos_hint={"x": 0.8, "y": 0},
            size_hint=(None, None),
        )
        self.top_bar.add_widget(self.score_label)

        # create game board
        self.game_board = FloatLayout(size_hint_y=0.8)
        self.screen.add_widget(self.game_board)

        # create buttons
        self.color_button_map = {}
        for c, pos in COLOR_POS_MAP.items():
            btn = SimonButton(color=c, pos_hint=pos)
            self.game_board.add_widget(btn)
            self.color_button_map[c] = btn

        # bind event handler to Window
        Window.bind(on_resize=self.on_window_resize)

        return self.screen


if __name__ == "__main__":
    SimonApp().run()
