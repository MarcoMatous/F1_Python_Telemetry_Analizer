import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import fastf1 as ff1
import fastf1.plotting

# Enabling cache so that I can save the datas from fastf1 on my pc and whenever I run them I won't need to connect to fastf1.
ff1.Cache.enable_cache('cache') 

# Loading race and preparing data
year, wknd, ses, driver_1, driver_2 = 2021, 7, 'FP3', 'LAT', 'LEC'
colormap = mpl.cm.plasma # type: ignore

session = ff1.get_session(year, wknd, ses)
weekend = session.event
session.load()
lap_driver_1 = session.laps.pick_driver(driver_1).pick_fastest()
lap_driver_2 = session.laps.pick_driver(driver_2).pick_fastest()


# Get telemetry data for both drivers
what = input('Choose what to compare: ( DistanceToDriverAhead, nGear, Brake, Speed, Throttle, DRS, RPM, Distance, RelativeDistance)')
while True:
    if what in 'DistanceToDriverAhead,nGear,Brake,Speed,Throttle,DRS,RPM,Distance,RelativeDistance':
        break
    else:
        what = input('Incorrect input, maybe typo error or bad comparison choice\nPlease try again:')
        
x_1, y_1, color_1 = lap_driver_1.telemetry['X'], lap_driver_1.telemetry['Y'], lap_driver_1.telemetry[f'{what}']
x_2, y_2, color_2 = lap_driver_2.telemetry['X'], lap_driver_2.telemetry['Y'], lap_driver_2.telemetry[f'{what}']

# Create line segments for both drivers
points_1 = np.array([x_1, y_1]).T.reshape(-1, 1, 2)
segments_1 = np.concatenate([points_1[:-1], points_1[1:]], axis = 1)
points_2 = np.array([x_2, y_2]).T.reshape(-1, 1, 2)
segments_2 = np.concatenate([points_2[:-1], points_2[1:]], axis = 1)

# Create subplots
ff1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1') # type:ignore
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.75))
plot_title = fig.suptitle(f'Season\'s weekend:{weekend.name}  Y:{year} - {what} Comparison - {driver_1} vs {driver_2}', size=24, y=0.97)

# Adjust margins and turn off axis
for ax in [ax1, ax2]:
    ax.axis('off')

# Plot data for driver 1
ax1.plot(x_1, y_1, color='black', linestyle='-', linewidth=16, zorder=0)
lc1 = LineCollection(segments_1, cmap=colormap, norm=plt.Normalize(color_1.min(), color_1.max()), linestyle='-', linewidth=5) # type: ignore
lc1.set_array(color_1)
ax1.add_collection(lc1)

# Plot data for driver 2
ax2.plot(x_2, y_2, color='black', linestyle='-', linewidth=16, zorder=0)
lc2 = LineCollection(segments_2, cmap=colormap, norm=plt.Normalize(color_2.min(), color_2.max()), linestyle='-', linewidth=5) # type: ignore
lc2.set_array(color_2)
ax2.add_collection(lc2)

# Add color bars as legends
cbaxes1 = fig.add_axes([0.1, 0.05, 0.35, 0.05]) # type: ignore
cbaxes2 = fig.add_axes([0.55, 0.05, 0.35, 0.05]) # type: ignore
legend1 = mpl.colorbar.ColorbarBase(cbaxes1, norm=plt.Normalize(color_1.min(), color_1.max()), cmap=colormap, orientation="horizontal") # type: ignore
legend2 = mpl.colorbar.ColorbarBase(cbaxes2, norm=plt.Normalize(color_2.min(), color_2.max()), cmap=colormap, orientation="horizontal") # type: ignore

# Show the plot
plt.savefig(what + 'Comparison_ dirvers' + driver_1 + 'vs' + driver_2 + '.png', dpi = 300)
plt.show()

