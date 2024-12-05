from os import PathLike
from typing import Dict, Tuple, Final, TypeAlias

# Custom types
PathLikeString: TypeAlias = str | PathLike
PointInfo: TypeAlias = Dict[str, str]
ColorType: TypeAlias = Tuple[float, float, float, float]

# Window
TITLE: Final[str] = 'Argüe'
WIDTH: Final[int] = 1080
HEIGHT: Final[int] = 2340

HALF_WIDTH: Final[int] = WIDTH // 2
HALF_HEIGHT: Final[int] = HEIGHT // 2

PALETTE: Final[str] = 'Blue'
THEME: Final[str] = 'Dark'

# Minimum and maximum values
MIN_COUNT: Final[int] = 0
MAX_COUNT: Final[int] = 9999

# Color
COLOR_CORRECT: Final[ColorType] = 0.07, 0.83, 0.13, 1
COLOR_INCORRECT: Final[ColorType] = 1, 0, 0, 1
COLOR_EDIT: Final[ColorType] = 0.2, 0.6, 0.9, 0.8
COLOR_DELETE: Final[ColorType] = 0.9, 0.2, 0, 0.8

# Screens
MAIN_SCREEN: Final[str] = 'main'
HISTORY_SCREEN: Final[str] = 'history'
INFO_SCREEN: Final[str] = 'info'

# Info
INFO: Final[str] = '''
Track [color=00FF00]correct[/color] and [color=FF0000]incorrect[/color] points during your discussions!


Use the [color=00FF00]correct[/color] counter when:
- Someone makes a valid point or wins an argument
- A statement is proven to be true or helpful in the discussion

Use the [color=FF0000]incorrect[/color] counter when:
- Someone is proven wrong or loses an argument
- A statement turns out to be false or irrelevant


[color=0066CC]Add reasons for each point to make it more fun to review later![/color]
'''
