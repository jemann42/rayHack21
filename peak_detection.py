# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 09:36:33 2021

@author: david
"""

import plotly.graph_objects as go
import pandas as pd
from scipy.signal import find_peaks

col_names = ['Data No',
             'Image Energy',
             'Last Average',
             'Time']

walabot_data = pd.read_csv('walabot.csv', names = col_names, skiprows=[0])

time_series = walabot_data['Last Average']

indices = find_peaks(time_series, distance=20, prominence=(0.002, 1), height=0.05 )[0]

print("Peak Indices :", indices)
print("Number of Peaks :", len(indices))
print("Number of Breaths :", len(indices) / 2)

sum_time = walabot_data.sum(axis = 0, skipna = True)

print("Total Time :",sum_time['Time'])

breath_rate = ((len(indices) / 2) / sum_time['Time']) * 60

print("Breath Rate (Breath Per Minute):", breath_rate)

fig = go.Figure()
fig.add_trace(go.Scatter(
    y=time_series,
    mode='lines+markers',
    name='Original Plot'
))

fig.add_trace(go.Scatter(
    x=indices,
    y=[time_series[j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
))

fig.show()