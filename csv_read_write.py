# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 20:50:38 2021

@author: david
"""

import pandas as pd

col_names = ['Data No',
             'Image Energy',
             'Running Min',
             'Running Max']

walabot_data = pd.read_csv('walabot.csv', names = col_names, skiprows=[0])
print(walabot_data)


for i in range(100):
    walabot_data.loc[i, 'Running Max'] = i
    
print(walabot_data)
walabot_data.to_csv('walabot.csv', index=False)