import inspect

from PIL import Image
from PIL.PngImagePlugin import PngInfo

import bases

method_list = [attribute for attribute in dir(bases) if callable(getattr(bases, attribute)) and attribute.startswith('__') is False]
print(type(method_list[4]))
func = getattr(bases,method_list[4])
sig = inspect.signature(func)
for position, (name, param) in enumerate(sig.parameters.items()):
    print(f"{position} {name}")
import sys
print("Python version")
print (sys.version)

targetImage = Image.open("..\spells\spell_level_blank_from_the_blank_school,_range_of_0_area_type_with_blank_damage_type_legend-False_breakdown-True.png")
metadata = PngInfo()
metadata.add_text("MyNewString", "A string")

# targetImage.save("img1.sw","PNG", pnginfo=metadata)
targetImage2 = Image.open("img1.sw")


print(targetImage.text)