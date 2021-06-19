# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:13:52 2021

@author: david
"""

import time  
import WalabotAPI as wlbt
from scipy.signal import find_peaks
import os

#           R [cm]     Phi [deg]  Theta [deg]
ARENA = [(20, 80, 1), (-4, 4, 1), (-4, 4, 1)]

# Samples collection window
SAMPLES = 512
ROLLING_AVE = 10

# Select Walabot wlbt.Init()  # load the WalabotSDK to the Python wrapper
wlbt.Init()
wlbt.Initialize()  # set the path to the essential database files

# Check if a Walabot is connected
try:
    wlbt.ConnectAny()
except wlbt.WalabotError as err:
    print("Failed to connect to Walabot.\nerror code: " + str(err.code))

print("Connected to Walabot")
wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)

# Set scan 
wlbt.SetArenaR(20, 80, 2)
wlbt.SetArenaPhi(-4, 4, 1)
wlbt.SetArenaTheta(-4, 4, 1)
print("Arena set")

# Set image filter
wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE)

# Start scan
wlbt.Start()
wlbt.StartCalibration()

samples = SAMPLES
rolling_ave = ROLLING_AVE
energy_log = []
time_log = []
average_energy_log = []
i = 0
last_time = time.time()

while True:
        
    for i in range(samples):
        wlbt.Trigger()
        energy = wlbt.GetImageEnergy()
        
        if len(energy_log) <= samples:
            energy_log.append(energy)
        if len(energy_log) == samples + 1:
            energy_log.pop(0)
        if len(energy_log) > samples:
            energy_log = energy_log[-samples:]
        
        # Average last three samples for a smoother response
        enrg = sum(energy_log[-rolling_ave:]) / rolling_ave
        
        # Average last three samples for a smoother response
        if i <= rolling_ave:
            enrg = energy
        else:
            enrg = sum(energy_log[-rolling_ave:]) / rolling_ave
            
        if len(average_energy_log) <= samples:
            average_energy_log.append(enrg)
        if len(average_energy_log) == samples + 1:
            average_energy_log.pop(0)
        if len(average_energy_log) > samples:
            average_energy_log = average_energy_log[-samples:]
            
        if len(time_log) <= samples:
            time_log.append(time.time() - last_time)
        if len(time_log) == samples + 1:
            time_log.pop(0)
        if len(time_log) > samples:
            time_log = time_log[-samples:]
            
        last_time = time.time()

    time_series = average_energy_log
    indices = find_peaks(time_series, distance=15, prominence=(0.002, 1), height=0.05 )[0]
    os.system('cls||clear')
    print("Peak Indices :", indices)
    print("Number of Peaks :", len(indices))
    sum_time = sum(time_log)
    breath_rate = ((len(indices) / 2) / sum_time) * 60
    print("Breath Rate (Breath Per Minute):", breath_rate)
    
wlbt.Stop()  # stops Walabot when finished scanning
wlbt.Disconnect()  # stops communication with Walabot