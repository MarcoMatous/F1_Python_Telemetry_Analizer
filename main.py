# We import the packages we need/ install them
# I run 'pip install [ package-name]' in command line

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils 
from matplotlib import pyplot as plt 
from matplotlib.pyplot import figure 
import numpy as np 
import pandas as pd

# Enabling cache so that I can save the datas from fastf1 on my pc and whenever I run them I won't need to connect to fastf1.
ff1.Cache.enable_cache('cache') 


####################################################
## Collecting the data ##
year, grand_prix, session = 2022,'Saudi Arabia', 'Q'
quali = ff1.get_session(year, grand_prix, session)
quali.load()
driver_1, driver_2 = 'PER', 'LEC'

# Accessing the laps with the .laps object coming from the session
laps_driver_1 = quali.laps.pick_driver(driver_1)
laps_driver_2 = quali.laps.pick_driver(driver_2)

# Select the fastest lap
fastest_driver_1 = laps_driver_1.pick_fastest()
fastest_driver_2 = laps_driver_2.pick_fastest()

# Retrieve the telemetry and add the distance column
telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

# Assigning the right color to the team-driver telemetry charts
team_driver_1 = fastest_driver_1['Team']
team_driver_2 = fastest_driver_2['Team']

# Delta time laps
'''This line shows the gap to the other driver in seconds throughout the lap. Important side note: this delta is an estimation, and therefore not too accurate. It does not represent the exact gap at any moment of a lap, but it shows us where a driver gained or lost time compared to another.'''
delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)


####################################################
## Plotting the data ##

