import pandas as pd
from os import listdir
from PIL import Image, ImageStat
from math import sqrt

data = [
    [
        'filename',
        'desc',
        'id',
        'width',
        'height',
        'mean',
        'median',
        'x_max',
        'y_max'
    ]
]

for filename in listdir('../../images'):
    if filename == '.DS_Store':
        continue
    path = '../../images/' + filename

    desc = ' '.join(filename[12:].split('-')[:-1])
    idd = filename.split('-')[-1][:-4]
    image = Image.open(path)
    width, height = image.size
    mean = ImageStat.Stat(image).mean
    mean = tuple([int(x) for x in mean])
    image_greyscale = Image.open(path).convert('LA')
    median = ImageStat.Stat(image_greyscale).median[0]
    
    pixels = image.getdata()
    minimum = 1000000000000
    x_max = 0 # poziomo
    y_max = 0 # pionowo
    for i, pixel in enumerate(pixels):
        if pixel == (255, 255, 255):
            x = i % width
            y = i // width
            norma = sqrt(x**2 + y**2)
            if norma < minimum:
                minimum = norma
                x_max = x 
                y_max = y

    # print(x_max, y_max)
    
    data.append([
        filename,
        desc,
        idd,
        width,
        height,
        mean,
        median,
        x_max,
        y_max
    ])

df = pd.DataFrame(data[1:], columns=data[0]) 
df.to_csv('images.csv', index=False)