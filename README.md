# SpellWritingGuide

This is the tidier version of the code used in the [Spell Writing Guide](https://www.drivethrurpg.com/product/429711/The-Spell-Writing-Guide?manufacturers_id=22808) which aims to provide a simple method by which we can draw spells in D&D 5e. The system is general to any system and easy to modify, I will explain this later.

## Setup

You can clone the repo for use simply by typing:

```git clone https://github.com/Duke-Archibald/SpellWritingGuideGui```

When initially running the code a folder called "Uniques" with files such as "11.npy" being created within. These contain the rotationally unique binary numbers the method relies on. They will only be created when such a file does not already exist in a directory called "Uniques".

### Dependencies

Python version used in development: Python 3.11.4 
but should run with anything more than 3.9

The required python modules are:
  - pyqt5
  - numpy
  - matplotlib
  - argparse
  - math
  - os
  - tqdm
  - qdarkstyle
  - asyncqt
  - asyncio
  - inspect
  - matplotlib.backends.backend_qt5agg
 
## Running the file

to run you type the command: ```py MainGui.py```

or you can double-click the ```MainGui.py``` file in the root folder

  
## Modifying
  
You can add your own options to the inputs by adding them in a new line in the relevant .txt files in "Attributes/"
  
  

