# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 09:36:33 2021

@author: david
"""

import plotly.graph_objects as go
import pandas as pd
from scipy.signal import find_peaks
from scipy.signal import butter, lfilter

col_names = ['Data No',
             'Image Energy',
             'Last Average',
             'Time']

walabot_data = pd.read_csv('walabot_fast.csv', names = col_names, skiprows=[0])

time_series = walabot_data['Last Average']

fs = 157.08 #sampling frequency
nyq = fs / 2
high_cut = 12.5663706 #high frequency
high = high_cut / nyq
b, a = butter(7, high , btype='low')

lp_filter_data = lfilter(b, a, time_series)

print("Low Pass Filter: ", lp_filter_data)

indices = find_peaks(lp_filter_data, distance=20, prominence=(0.002, 1), height=0.05)[0]

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
    name='Original Plot (Rolling 10 Average)'
))

fig.add_trace(go.Scatter(
    y=lp_filter_data,
    mode='lines+markers',
    name='LP Filter'
))

fig.add_trace(go.Scatter(
    x=indices,
    y=[lp_filter_data[j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
))

fig.show()