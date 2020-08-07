def info(*args):
    for msg in list(args):
        print(msg)

def error(*args):
    for msg in list(args):
        print('\033[91m{}\033[0m'.format(msg))

def success(*args):
    for msg in list(args):
        print('\033[92m{}\033[0m'.format(msg))

def warning(*args):
    for msg in list(args):
        print('\033[93m{}\033[0m'.format(msg))