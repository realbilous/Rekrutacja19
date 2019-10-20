import pandas as pd
from shutil import copyfile, rmtree
from os import mkdir, path


def my_mkdir(no_folders):
    if path.exists(f'{no_folders}-images'):
        rmtree(f'{no_folders}-images')
    mkdir(f'{no_folders}-images')


data = pd.read_csv('images.csv')
data = data.sort_values(by='median')
no_folders = 1
no_files = 0
my_mkdir(no_folders)
no_files = 0
for index, row in data.iterrows():
    copyfile(f'../../images/{row["filename"]}', f'{no_folders}-images/{row["filename"]}')
    no_files += 1
    if no_files >= 4:
        no_files = 0
        no_folders += 1
        if no_folders > 5:
            break
        my_mkdir(no_folders)