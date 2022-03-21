import enum


class Clicker(enum.Enum):
    SIMON = enum.auto()
    PLAYER = enum.auto()

    def __str__(self):
        return f"{self.name.capitalize()} Says"


class Colors(enum.Enum):
    BLUE = enum.auto()
    GREEN = enum.auto()
    RED = enum.auto()
    YELLOW = enum.auto()

    def __str__(self):
        return self.name.lower()

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name.lower(), cls))


COLORS = {
    "blue_unpressed": [0, 62 / 255, 179 / 255, 1],
    "blue_pressed": [48 / 255, 121 / 255, 1, 1],
    "green_unpressed": [0, 168 / 255, 11 / 255, 1],
    "green_pressed": [75 / 255, 1, 91 / 255, 1],
    "red_unpressed": [176 / 255, 0, 0, 1],
    "red_pressed": [1, 60 / 255, 54 / 255, 1],
    "yellow_unpressed": [219 / 255, 219 / 255, 0, 1],
    "yellow_pressed": [1, 1, 71 / 255, 1],
}
LABEL_TEXT = "[color=000000]{}[/color]"
BOLD_LABEL_TEXT = "[b][color=000000]{}[/color][/b]"
COLOR_POS_MAP = {
    str(Colors.BLUE): {"x": 0.23, "y": 0.2},
    str(Colors.GREEN): {"x": 0.53, "y": 0.2},
    str(Colors.RED): {"x": 0.23, "y": 0.6},
    str(Colors.YELLOW): {"x": 0.53, "y": 0.6},
}
