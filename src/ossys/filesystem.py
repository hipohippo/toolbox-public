import glob
import os


# 1. list files under given directory

# good way
from pathlib import Path

glob.glob()

# not-so-good way
os.listdir()


# walk all files recursively in the folder
#
# [f.name for f in p.glob("**/*")]  # or
# [f.name for f in p.rglob("*")]

# get file name only without suffix
f = Path(...)
f.stem
f.suffix
f.name