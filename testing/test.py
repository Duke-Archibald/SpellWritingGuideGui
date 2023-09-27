import inspect

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
