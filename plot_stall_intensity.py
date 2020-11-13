""" script which reads in the stalling csv file and plots a stall intensity graph

author : emily vosper
""" 

# import modules
import numpy as np
import pandas as pd
import hurricane
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# get data
stall_df = pd.read_csv('data/stalled_hurricanes.csv')
stall_df = stall_df[stall_df['year']>=1970]
stall_intensity = stall_df['max_wind']
colours = ['#008CFF','#FF7700','#53E016','red','brown']

x = stall_df['year']
y = stall_intensity*1.852
alpha = 0.5
plt.scatter(x,y,marker='o',alpha=alpha,color='#008CFF',facecolor='white')

# if (storm_name[i],years[i]) in [('Harvey',2017),('Mitch',1998),("Dorian",2019),('Opal',1995),('Paloma',2008),('Felix',1995)]:
for storm in ['Dorian','Ophelia','Harvey','Paloma','Felix','Opal']:
    storm_idx = stall_df.index[stall_df['name']==storm].to_list()[-1] # select the most recent hurricane if it has a popular name    
    print(storm_idx)
    x2 = x[storm_idx]
    y2 = y[storm_idx]
    plt.annotate('%s' % storm, xy=(x2-3,y2-8),xycoords='data',fontsize=8,alpha=0.7,color='purple')
    plt.scatter(x2,y2,marker='o',alpha=alpha,color='purple',facecolor='white')
    alpha=0.8


print("number of stalling hurricanes",len(stall_df))

plt.xticks(range(1970,2030,10),fontsize=10)
plt.xlabel('Year',size=12)
plt.ylabel('Maximum sustained wind speed kmh$^{-1}$',size=12)
plt.savefig('figs/stall_intensity.png',dpi=600,bbox_inches = 'tight')
print('plot saved!')