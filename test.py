import random
from termcolor import colored

L = ['a', 'b', 'c']
for i in range(0, 100):
    x = random.sample(L, 1)

print(colored('[■■■■■■■■■         ]', 'red'))
print(colored('[■■■■■■■■■■■■■     ]', 'blue'))
