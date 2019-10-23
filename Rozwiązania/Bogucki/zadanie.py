#!/usr/bin/env python
# coding: utf-8

# # zadanie 1

# In[195]:


import re
import numpy as np
import pandas as pd
from PIL import Image
from os import listdir, mkdir
from os.path import join
import csv
from shutil import move


# In[167]:


path = "images"
files = listdir(path)
n = len(files)
file_names = files
file_desc = list(map(lambda x: re.findall("(?<=stock-photo-)[\w|-]+(?=-[0-9]+\.jpg)",x)[0],files))
file_desc = list(map(lambda x: re.sub("-"," ",x),file_desc))
file_id = list(map(lambda x: re.findall("(?<=-)[0-9]+(?=.jpg)",x)[0],files))


# In[168]:


heights = [None]*n
widths = [None]*n
mean_color = [None]*n
medians = [None]*n
brighter_row = [None]*n
brighter_col = [None]*n
for i in range(n):
    image = Image.open(join(path, files[i]))
    widths[i] = image.size[0]
    heights[i] = image.size[1]
    img_raw = np.array(image)
    mean_color[i] = '#%02x%02x%02x' % tuple(np.mean(img_raw, axis=(0,1),dtype=int))
    img_grey = image.convert('L')
    img_grey_raw = np.array(img_grey)
    medians[i] = np.median(img_grey_raw)
    max_val = np.max(img_grey_raw)
    max_coord = np.asmatrix(np.where(img_grey_raw==max_val))
    min_dist = np.Inf
    min_col = 0
    for j in range(max_coord.shape[1]):
        x = max_coord[0,j]
        y = max_coord[1,j]
        if np.sqrt(x**2+y**2) < min_dist:
            min_col=j
            min_dist = np.sqrt(x**2+y**2)
    brighter_row[i] = max_coord[0,min_col]
    brighter_col[i] = max_coord[1,min_col]


# In[169]:


data = {'name': file_names, 
        'description': file_desc, 
        'id': file_id, 
        'width': widths , 
        'height': heights, 
        'mean color': mean_color,
       'median': medians,
       'brightest x': brighter_row,
       'brightest y': brighter_col}
data = pd.DataFrame(data)
data


# In[194]:


data.to_csv("images.csv", index=False)


# # zadanie 2

# In[187]:


data_sorted = data.sort_values(by=['median'])
names_sorted = data_sorted.loc[:,'name']
names_sorted


# In[203]:


for i in range(5):
    dir_name = "{}-images".format(i+1)
    mkdir(join(path,dir_name))
    for j in range(4):      
        move(join(path,names_sorted.iloc[i*4+j]),join(path,dir_name,names_sorted.iloc[i*4+j]))

