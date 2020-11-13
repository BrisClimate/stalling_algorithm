"""
Set of hurricane functions

	author : emily vosper
"""

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point


def stall_point2(lats,lons):
    """
    Function which calculates the stall points along a hurricane track and returns the point of stalling

	inputs
	------
			lats : array-like vector of latitudes
			lons : array-like vector of latitudes

	output
	------
			stall_idx : the index of the lat and lon vector where the hurricane begins to stall
            circle : geometry polygon of stall region
    """
    # initialise variables
    end = np.where(lats.mask==True)[0][0]
    stall_region = []
    circles = []

    # loop through points along storm track
    for j in range(8,end-8): #0 -> end-max
        point = Point([lats[j],lons[j]]) # (lat,lon) for storm i at time j
        for n in range(1,9):    
            exec('global point%s; point%s = Point([lats[j+%s],lons[j+%s]])' % (n,n,n,n)) # points 3,6,9,12,15,18,21,24 hours after
            exec('global point%s; point%s = Point([lats[j-%s],lons[j-%s]])' % (n+8,n+8,n,n)) # points 3,6,9,12,15,18,21,24 hours before
        circle = point.buffer(1.8) # 200 km radius

        # stalls if point is within 200km of the next 6 time points (24hours)
        stalls  =  (circle.contains(point) and circle.contains(point1) and circle.contains(point2) and 
                    circle.contains(point3) and circle.contains(point4) and circle.contains(point5) and
                    circle.contains(point6) and circle.contains(point7) and circle.contains(point8) and 
                    circle.contains(point9) and circle.contains(point10) and circle.contains(point11) and
                    circle.contains(point12) and circle.contains(point13) and circle.contains(point14) and
                    circle.contains(point15) and circle.contains(point16))

        # log stall
        if stalls == True:
            # make sure to get all distinct stalls
            if j-1 in stall_region:
                continue
            else:
                stall_region.append(j-2) # j is the centroid of the stall, to get the point at which the hurricane starts to stall use j-2
                circles.append(circle)
    
    if stall_region != []:
        return stall_region,circles
    else:    
        return False       

def configure_stall_plot():
    """
    load basemap configurations
    """
    m = Basemap(llcrnrlon=-100.,llcrnrlat=5.,urcrnrlon=-50.,urcrnrlat=40.,
			projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
			resolution ='l',area_thresh=1000.)
    m.drawparallels(np.arange(-60.,120.,10.),linewidth=0.3,dashes=[5,5],labels=[1,0,0,0],size=8)
    m.drawmeridians(np.arange(0.,360.,10.),linewidth=0.3,dashes=[5,5],labels=[0,0,0,1],size=8)
    m.bluemarble()
    return m

def plot_stall(name,circle,lat,lon,i,j):
    """
    plot of stalling hurricanes
    """
    m = configure_stall_plot()
    x,y = circle.exterior.xy
    y,x = m(y,x)
    plt.plot(y,x,alpha=0.8,linewidth=0.8,color='white')
    xp,yp = m(lon[i,j],lat[i,j])

    x,y = m(lon[i],lat[i])
    m.plot(x,y,marker='',color='orange',linewidth=0.5, alpha=1)
    x2 = x[::2]
    y2 = y[::2]
    m.scatter(x2,y2,marker='o',color='orange',s=0.7)
    sx,sy = m(lon[i,j],lat[i,j])
    m.scatter(sx,sy,marker='o',color='purple',s=0.7,zorder=5)

    if name == 'Harvey':
        xp,yp = m(lon[i,j]-4.6,lat[i,j]+1.4)
    else:
        xp,yp = m(lon[i,j]+1.6,lat[i,j]+1.4)  

    if name == 'Mitch':
        print(j,"j")
        if j == 35:
            plt.annotate('%s' % name, xy=(xp,yp),xycoords='data',color='orange',fontsize=6)
    else: 
        plt.annotate('%s' % name, xy=(xp,yp),xycoords='data',color='orange',fontsize=6)
        
def extract_tracks(data):
    """
    Extract track data from netcdf file 

    input
    -----
    		data : netcdf file 

	output
	------
			storm_name : string
            time : array
            lat : array
            lon : array
            max_wind : float
            cat : int (storm category)
            gust : array
            year : int
    """

    with Dataset(data,'r') as f:
        max_wind = f.variables['usa_wind'][:] # max sustained wind speed
        cat = f.variables['usa_sshs'][:] # hurricane category
        gust = f.variables['usa_gust'][:] # max gust
        storm_name = f.variables['name'][:]
        lat = f.variables['usa_lat'][:]
        lon = f.variables['usa_lon'][:]
        time = f.variables['time'][:]
        year = f.variables['season'][:]

    new_names = []
    for name in storm_name:
        new_name = ''
        for letter in name:
            if np.ma.is_masked(letter):
                continue
            new_letter = letter.decode("utf-8")
            if len(new_name) == 0:
                new_name += new_letter
            else:
                new_name += new_letter.lower()
        new_names.append(new_name)
    storm_name = new_names

    return storm_name,time,lat,lon,max_wind,cat,gust,year



