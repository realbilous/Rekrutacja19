import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict
import cv2
import shutil

imgs_dict = defaultdict(lambda: [])
imgs_folder = Path('./images')

for idx, f_name in enumerate(imgs_folder.iterdir()):
    imgs_dict['Nazwa pliku'].append(f_name.name)
    imgs_dict['Opis zawartości zdjęcia (separator “-” należy zamienić na spację)'].append(f_name.stem.replace('-', ' '))
    imgs_dict['Id zdjęcia'].append(idx)

    img = cv2.imread(str(f_name))

    imgs_dict['Szerokość'].append(img.shape[1])
    imgs_dict['Wysokość'].append(img.shape[0])

    print(img.shape[1])
    print(img.shape[0])

    avg_color = np.mean(np.mean(img, axis=0), axis=0)

    imgs_dict['Średni kolor'].append(avg_color)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgs_dict['Mediana jasności po przekonwertowaniu na odcienie szarości'].append(np.median(gray_img))

    max_idx_cols = np.argmax(gray_img, axis=1)
    max_v_cols = gray_img[np.arange(gray_img.shape[0]), max_idx_cols]
    only_max_v_cols = max_idx_cols * np.where(max_v_cols < np.amax(max_v_cols), np.nan, 1)
    _, hh, ww = min([((idx_row**2 + idx_col**2)**(1/2), idx_row, idx_col)
                     for idx_row, idx_col in enumerate(only_max_v_cols)
                     if not np.isnan(idx_col)])

    imgs_dict['Pozioma współrzędna najjaśnieszego pixela po przekonwertowaniu na odcienie szarości*'].append(ww)
    imgs_dict['Pionowa współrzędna najjaśnieszego pixela po przekonwertowaniu na odcienie szarości*'].append(hh)

df_imgs = pd.DataFrame(imgs_dict)
df_imgs.to_csv('images.csv', index=False)
pth = Path('./kubelki')


df_sorted_imgs = df_imgs.sort_values(by='Mediana jasności po przekonwertowaniu na odcienie szarości')
df_sorted_imgs_names = df_sorted_imgs['Nazwa pliku']
i = 0
for idx, img_name in enumerate(df_sorted_imgs_names):

    if not idx%4:
        i += 1

    path_k = pth/f'{i}-images'
    path_k.mkdir(parents=True, exist_ok=True)

    src = imgs_folder/img_name
    dest = path_k/img_name
    shutil.move(src, dest)