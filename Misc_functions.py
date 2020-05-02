from termcolor import cprint


def unfucked_input(text):
    while True:
        try:
            x = input(text)
            break
        except EOFError:
            cprint('stop trying to break my program dickhead', 'red')
            continue
    return x
