"""
    Settings.py provides a global variable store to define static variables
    and setup variables that needs to be overwritten in the implementation
"""

import pathlib


# Base variables
BASE_DIR = pathlib.Path(__file__).parent.absolute()
RESOURCE_DIR = BASE_DIR.joinpath('resources')
TEMPLATE_DIR = RESOURCE_DIR.joinpath('templates')

# Project variables - Override
