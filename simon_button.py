from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button

from constants import COLORS, Clicker


class SimonButton(Button):
    def __init__(self, **kwargs):
        # methods obtained from SimonApp
        self.game_over_func = (
            None
            if "game_over_func" not in kwargs.keys()
            else kwargs.pop("game_over_func")
        )
        self.start_round = (
            None if "start_round" not in kwargs.keys() else kwargs.pop("start_round")
        )
        self.check_player_seq = (
            None
            if "check_player_seq" not in kwargs.keys()
            else kwargs.pop("check_player_seq")
        )
        self.on_trigger_action = (
            None
            if "on_trigger_action" not in kwargs.keys()
            else kwargs.pop("on_trigger_action")
        )

        super().__init__(**kwargs)

        self.color_name = kwargs["color"]
        self.new_round = False
        self.clicker = Clicker.SIMON
        self.game_over = False

        self.background_color = COLORS[
            f"{self.color_name}_unpressed"
        ]  # setting background color using rgba
        self.background_down = ""
        self.background_normal = ""
        self.size_hint = (0.25, 0.3)

        Window.clearcolor = [1, 1, 1, 1]

    def on_simon_press(self):
        """
        Method called when Simon presses the button.
        This prevents unexpected behaviour if the player presses a button during Simon's turn
        """
        self.background_color = COLORS[f"{self.color_name}_pressed"]

        Clock.schedule_once(self.reset_color, 0.3)

        if self.clicker == Clicker.SIMON and self.on_trigger_action:
            self.on_trigger_action()

    def on_press(self):
        """
        Method called when the player presses the button.
        """
        self.background_color = COLORS[f"{self.color_name}_pressed"]

        Clock.schedule_once(self.reset_color, 0.3)

        if self.clicker == Clicker.PLAYER and self.check_player_seq != None:
            self.check_player_seq(self.color_name)

    def reset_color(self, instance):
        """
        Reset color of the buttons after each round/game
        """
        self.background_color = COLORS[f"{self.color_name}_unpressed"]
        if self.clicker == Clicker.PLAYER and self.new_round:
            # new round
            self.start_round()
            self.new_round = False
        elif self.clicker == Clicker.PLAYER and self.game_over:
            # game over
            self.game_over_func()
            self.game_over = False
