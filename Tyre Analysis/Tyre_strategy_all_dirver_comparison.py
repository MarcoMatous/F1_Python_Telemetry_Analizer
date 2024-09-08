YEAR = 2018
PRIX = 'France'
TYPE = 'R'

from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting

session = fastf1.get_session(YEAR, PRIX, TYPE)
session.load()
laps = session.laps

# Loading drivers and printing the abbreviation for each dirver
drivers = session.drivers
drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
#print(drivers)

#We need to find the stint length and compound used for every stint by every driver. We do this by first grouping the laps by the driver, the stint number, and the compound. And then counting the number of laps in each group.
stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})
print(stints)

# plotting the strategies for each driver
fig, ax = plt.subplots(figsize=(5, 10))

for driver in drivers:
    driver_stints = stints.loc[stints["Driver"] == driver]
    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        # each row contains the compound name and stint length
        # we can use these information to draw horizontal bars
        compound_color = fastf1.plotting.get_compound_color(row["Compound"],session=session)
        plt.barh(y=driver,width=row["StintLength"], left=previous_stint_end, color=compound_color, edgecolor="black", fill=True)
        previous_stint_end += row["StintLength"]
        
plt.title(str(YEAR) + ' ' + PRIX + " Grand Prix Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
# invert the y-axis so drivers that finish higher are closer to the top
ax.invert_yaxis()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.show()


