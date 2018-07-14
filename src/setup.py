"""Fichier d'installation de notre script salut.py."""


from cx_Freeze import setup, Executable


# On appelle la fonction setup

setup(

    name = "EasyBeer",

    version = "1.0.0",

    description = "A beer brewer assistant",

    options = {"build_exe": {'include_files':('translate','translate')}},

    executables = [Executable("main.py")],

    )
