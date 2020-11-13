""" script which reads in best tracks data and finds the stalling huricanes

author : emily vosper
"""  

import hurricane
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
from shapely.geometry import shape,Point

# define initial variables
storm_name,time,lat,lon,max_wind,cat,gust,year = hurricane.extract_tracks('data/ibtracks_na.nc')
storm_range = range(2220)
stall_tally = []
stall_points = []
stall_regions = []

# loop through each storm and determine if they stalled
print('Looping though storms to find stalling hurricanes...')
for i in storm_range:
	print(i,end='\r')
	count = np.ma.filled(lat[i,:],fill_value=0)
	end = np.where(count == 0.)[0][0]
	stall_region = []
	stall = hurricane.stall_point2(lat[i],lon[i])
	if stall != False:
		stall_idxs,circles = stall
		stall_idx = stall_idxs[0] # select the first stall (if a hurricane happens to stall more than once)
		circle = circles[0]
		stall_tally.append(i)
		stall_points.append(stall_idx)
		stall_regions.append(circle)

# define and save pandas dataframe
print('Okay!')
print('Stalling hurricanes found, saving dataframe...')
hurricane_category = cat[stall_tally,stall_points]
max_winds = max_wind[stall_tally,stall_points]
storm_names = np.array(storm_name)[stall_tally]
years = year[stall_tally]
lats = lat[stall_tally]
lons = lon[stall_tally]
stall_df = pd.DataFrame({
	'name'	: storm_names,
	'year'	: years,
	'hurricane_idx' : stall_tally,
	'stall_idx' : stall_points,
	'max_wind'	: max_winds,
	'category'	: hurricane_category
})
stall_df.to_csv('data/stalled_hurricanes.csv')
print('Saved!')

# choose the hurricanes to plot 
print('Plotting a selection of stalls...')
for storm in ['Dorian','Ophelia','Harvey','Paloma','Felix','Opal']:
	storm_idx = stall_df.index[stall_df['name']==storm].to_list()[-1] # select the most recent hurricane if it has a popular name
	circle = stall_regions[storm_idx]
	stall_idx = stall_df['stall_idx'][storm_idx]
	hurricane.plot_stall(storm,circle,lats,lons,storm_idx,stall_idx)

plt.savefig('figs/stall_map.png',dpi=600,bbox_inches='tight')
plt.clf()
print('Plot saved!')


		


