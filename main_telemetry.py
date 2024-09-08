# We import the packages we need/ install them
# I run 'pip install [ package-name]' in command line

'''
NB, TO DO, TASKS: 
1) ADD USEFUL STUFF FROM FASF1 DOC EXMPLES
2) REFINE

'''

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils 
from matplotlib import pyplot as plt 
from matplotlib.pyplot import figure 
from matplotlib.collections import LineCollection
from matplotlib import cm
import numpy as np 
import pandas as pd



# Enabling cache so that I can save the datas from fastf1 on my pc and whenever I run them I won't need to connect to fastf1.
ff1.Cache.enable_cache('cache') 


####################################################
## Collecting the data ##
year, grand_prix, session = 2021,'France', 'FP3'
quali = ff1.get_session(year, grand_prix, session)
quali.load()
driver_1, driver_2  = 'LAT', 'LEC'
    #driver_3 = 'VET'
    
# Accessing the laps with the .laps object coming from the session
laps_driver_1 = quali.laps.pick_driver(driver_1)
laps_driver_2 = quali.laps.pick_driver(driver_2)
    # laps_driver_3 = quali.laps.pick_driver(driver_3)

# Select the fastest lap
fastest_driver_1 = laps_driver_1.pick_fastest()
fastest_driver_2 = laps_driver_2.pick_fastest()
    # fastest_driver_3 = laps_driver_3.pick_fastest()

# Retrieve the telemetry and add the distance column
telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()
    # telemetry_driver_3 = fastest_driver_3.get_telemetry().add_distance()

# Assigning the right color to the team-driver telemetry charts
team_driver_1 = fastest_driver_1['Team']
team_driver_2 = fastest_driver_2['Team']
    # team_driver_3 = fastest_driver_3['Team']

# Delta time laps
'''This line shows the gap to the other driver in seconds throughout the lap. Important side note: this delta is an estimation, and therefore not too accurate. It does not represent the exact gap at any moment of a lap, but it shows us where a driver gained or lost time compared to another.'''
delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)


####################################################
## Plotting the data ##
plotting.setup_mpl(color_scheme='fastf1',misc_mpl_mods=False)
plot_size = [15,15]
plot_title = f"{quali.event.year} {quali.event.EventName} - {quali.name} - {driver_1} vs {driver_2}"
plot_ratios = [1,3,2,1,1,2,1]
    #specifies the size of the subplots 
plot_filename = plot_title.replace(' ', '') + ".png"
plt.rcParams['figure.figsize'] = plot_size
fig, ax = plt.subplots(7, gridspec_kw={'height_ratios':plot_ratios})

#setting the plot title
ax[0].title.set_text(plot_title)


# Plotting the delta line
ax[0].plot(ref_tel['Distance'],delta_time)
ax[0].axhline(0)
ax[0].set(ylabel = f"Gap to {driver_2} (s)")
ax[0].legend(loc='lower right')


#Speed trace    
ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label = driver_1, color = ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label = driver_2, color = ff1.plotting.team_color(team_driver_2)) # type: ignore
# ax[1].plot(telemetry_driver_3['Distance'], telemetry_driver_3['Speed'], label = driver_3, color = ff1.plotting.team_color(team_driver_3))

ax[1].set(ylabel = 'Speed')
ax[1].legend(loc='lower right')
ax[1].grid(True, linestyle = '--')


#Throttle trace
ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label = driver_1, color = ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label = driver_2, color = ff1.plotting.team_color(team_driver_2)) # type: ignore
# ax[2].plot(telemetry_driver_3['Distance'], telemetry_driver_3['Throttle'], label = driver_3, color = ff1.plotting.team_color(team_driver_3))
ax[2].set(ylabel = 'Throttle')
ax[2].legend(loc='lower right')

#Brake trace
ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label = driver_1, color = ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label = driver_2, color = ff1.plotting.team_color(team_driver_2)) # type: ignore
# ax[3].plot(telemetry_driver_3['Distance'], telemetry_driver_3['Brake'], label = driver_3, color = ff1.plotting.team_color(team_driver_3))
ax[3].set(ylabel = 'Brake')


#Gear trace
ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label = driver_1, color = ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label = driver_2, color = ff1.plotting.team_color(team_driver_2)) # type: ignore
ax[4].set(ylabel = 'Gear')


#RPM trace
ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1, color=ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2, color=ff1.plotting.team_color(team_driver_2)) # type: ignore
# ax[5].plot(telemetry_driver_3['Distance'], telemetry_driver_3['RPM'], label=driver_3, color=ff1.plotting.team_color(team_driver_3))
ax[5].set(ylabel='RPM')
ax[5].legend(loc='lower right')


#DRS trace
ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1, color=ff1.plotting.team_color(team_driver_1)) # type: ignore
ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2, color=ff1.plotting.team_color(team_driver_2)) # type: ignore
ax[6].set(ylabel='DRS')
ax[6].set(xlabel='Lap distance (meters)')



# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()
    
# Store figure
plt.savefig(plot_filename, dpi=300)
plt.show()

