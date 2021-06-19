# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 16:23:53 2021

@author: david
"""
import multiprocessing
import time
import sys
import zmq
import os
    
import WalabotAPI as wlbt

#           R [cm]     Phi [deg]  Theta [deg]
ARENA = [(20, 80, 1), (-4, 4, 1), (-4, 4, 1)]

# Samples collection window
SAMPLES = 60
    
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
wlbt.SetArenaR(20, 80, 1)
wlbt.SetArenaPhi(-4, 4, 1)
wlbt.SetArenaTheta(-4, 4, 1)
print("Arena set")

# Set image filter
wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_DERIVATIVE)

# Start scan
wlbt.Start()
wlbt.StartCalibration()

while True:
    wlbt.Trigger() 
    energy = wlbt.GetImageEnergy()
    print(energy)
    
wlbt.Stop()  # stops Walabot when finished scanning
wlbt.Disconnect()  # stops communication with Walabot

