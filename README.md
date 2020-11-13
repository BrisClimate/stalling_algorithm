# Hurricane Stall Algorithm

This repositry consists of three scripts that can be used to find stalling hurricanes and plot their trajectory or intensity.

## hurricane.py
This script contains the functions.

## find_stalling_hurricanes.py
You must run this script first to generate the stalling csv file. You can load in the ibtracks netCDF file found in data/ or upload your own.

## plot_stall_intensity.py
This script will make a plot of hurricane intensity at the point of stalling. Note that in this version it will only plot the intensity of the first hurricane stall, so if a hurricane stalls more than once it will only plot the first stall. This can be amended if needed.

## Versions:
numpy                    1.19.2

netcdf4                  1.5.3

matplotlib               3.0.3*

shapely                  1.6.4

basemap                  1.2.0

pandas                   1.1.3

*higher version of this don't work with basemap
