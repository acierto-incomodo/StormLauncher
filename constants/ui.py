from __future__ import annotations

import os
import platform

BG_COLOUR = "#2F3136"
FG_COLOUR = "#2c3e50"
THEME = "equilux"

if platform.system() == "Windows":
    BOX_WIDTH = 13
    ENTRY_LEN = 40
    BAR_LEN = 245
    LIST_LEN = 15
else:
    BOX_WIDTH = 7
    ENTRY_LEN = 30
    BAR_LEN = 245
    LIST_LEN = 8

LOGO_SMALL = os.path.join("img", "stormlauncher_logo.png")
LOGO_ICON = os.path.join("img", "stormlauncher_ico.ico")
