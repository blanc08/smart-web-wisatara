from os import path
import os
from constant import CATEGORIES


def make_output_dir():
    """
    prepare output directories
    """
    os.makedirs(path.join(path.curdir, "out"), exist_ok=True)
