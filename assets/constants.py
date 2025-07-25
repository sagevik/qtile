from typing import Dict

WALLPAPER = "/home/rs/.local/share/background/wp.png"
FONT_TYPE = "Hack Nerd Bold"
FONT_SIZE = 12


class ColourEnum:
    _colours: Dict[str, str] = {}

    def __init_subclass__(cls):
        for name, hex_value in cls.__annotations__.items():
            if isinstance(hex_value, str) and hex_value.startswith("#"):
                cls._colours[name] = hex_value

    def __getattr__(self, name: str) -> str:
        if name in self._colours:
            return self._colours[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


class Colours(ColourEnum):
    GREY = "#696969"
    AQUA = "#8ea4a2"
    BLUE_GREY = "#405569"
    YELLOW = "#c4b28a"
    DARK_BLUE = "#182838"
    VERY_DARK_BLUE = "#101c29"
    WHITE = "#c5c9c5"
    BLACK = "#1d1c19"
    BLACK6 = "#625e5a"
    WARNING = "#f6719b"
    VIOLET = "#8992a7"
    TEAL = "#949fb5"
    ORANGE = "#b6927b"
    GREEN = "#87a987"
    GRAY = "#a6a69c"
