#new file for easier graphical comparison with the other .py file

YEAR, WEEK, TYPE = 2018, 6, 'R'
import matplotlib.pyplot as plt
import fastf1.plotting


# Load FastF1's dark color scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False,color_scheme='fastf1')

# Load the session and create the plot
session = fastf1.get_session(YEAR, WEEK, TYPE)
session.load(telemetry=False, weather=False)

fig, ax = plt.subplots(figsize=(8.0, 4.9))
# sphinx_gallery_defer_figures

##############################################################################
# For each driver, getting their three letter abbreviation (e.g. 'HAM') by simply using the value of the first lap, get their color and then plot their position over the number of laps.
for drv in session.drivers:
    drv_laps = session.laps.pick_driver(drv)
    abb = drv_laps['Driver'].iloc[0]
    style = fastf1.plotting.get_driver_style(identifier=abb,style=['color', 'linestyle'],session=session)
    ax.plot(drv_laps['LapNumber'], drv_laps['Position'],label=abb, **style)
# sphinx_gallery_defer_figures

ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')
# sphinx_gallery_defer_figures

##############################################################################
# Adding the legend outside the plot area.
ax.legend(bbox_to_anchor=(1.0, 1.02))
plt.tight_layout()

plt.show()
