import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pyHook"], "include_msvcr": True}

setup(
    name = "ck2_mps",
    version = "0.1",
    description = "Crusader Kings II multiplayer speed control for all players.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("ck2_mps.py")])