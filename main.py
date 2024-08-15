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

# Collecting the data

