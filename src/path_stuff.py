import os

def make_abs(files):
    new_list = []
    for file in files:
        new_file = os.path.abspath(file)
        new_list.append(new_file)
    return new_list