import random
from termcolor import cprint

burning = {'active': True, 'duration': 3}
c = burning.copy()
while c['active']:
    cprint('AHHHHHHHHHHHHHH', 'red')
    c['duration'] -= 1
    if c['duration'] <= 0:
        print('oh thats done')
        c['active'] = False
print(burning)
