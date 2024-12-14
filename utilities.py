from os import PathLike
from typing import Dict, Tuple, Final, TypeAlias

# Custom types
PathLikeString: TypeAlias = str | PathLike
PointInfo: TypeAlias = Dict[str, str]
ColorType: TypeAlias = Tuple[float, float, float, float]

# Theme
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
SETTINGS_SCREEN: Final[str] = 'settings'

# Other
GITHUB_LINK: Final[str] = 'https://github.com/CrazyFlyKite/Argue'
