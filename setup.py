# -*- coding: utf-8 -*-
import os
import sys
from cx_Freeze import setup, Executable

path_origem = "./asset"
asset_list = os.listdir(path_origem)
include_files = [
    (os.path.join(path_origem, arquivo).replace("\\", "/"), os.path.join("asset", arquivo).replace("\\", "/"))
    for arquivo in asset_list
]

executables = [
    Executable(
        "main.py",
        base="gui" if sys.platform == "win32" else None,
        target_name="TheHungryRun.exe"
    )
]

files = {
    "include_files": include_files,
    "packages": ["pygame"],
    "includes": ["code"],
    "build_exe": "build/TheHungryRun"
}

setup(
    name="The Hungry Run",
    version="1.0",
    description="Ajude o T-Rex a correr e pegar a carne!",
    options={"build_exe": files},
    executables=executables
)