from json import load
from random import randint


with open("ua.json", "r") as f:
    res = load(f)

i = randint(0, len(res)-1)
print(res[i]['ua'])
