# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:23:53 2021

@author: david
"""

import time  
import WalabotAPI as wlbt
import pandas as pd

#           R [cm]     Phi [deg]  Theta [deg]
ARENA = [(20, 80, 1), (-4, 4, 1), (-4, 4, 1)]

# Samples collection window
SAMPLES = 1024
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

col_names = ['Data No',
             'Image Energy',
             'Last Average',
             'Time']
walabot_data = pd.read_csv('walabot.csv', names = col_names, skiprows=[0])


samples = SAMPLES
rolling_ave = ROLLING_AVE
energy_log= []
last_time = time.time()
    
    
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
    if i >= rolling_ave:
        enrg = sum(energy_log[-rolling_ave:]) / rolling_ave
    else:
        enrg = energy
    print(i, energy)
    walabot_data.loc[i, 'Data No'] = int(i + 1)
    walabot_data.loc[i, 'Image Energy'] = energy
    walabot_data.loc[i, 'Last Average'] = enrg
    walabot_data.loc[i, 'Time'] = time.time() - last_time
    last_time = time.time()
    
walabot_data.to_csv('walabot.csv', index=False)
    
wlbt.Stop()  # stops Walabot when finished scanning
wlbt.Disconnect()  # stops communication with Walabot

