from django.test import TestCase
import pyproj
import numpy as np
# Create your tests here.
import pycrs

# Define the crs for the GeoDataFrame as proj4-string
crs = pycrs.parse.from_epsg_code(23032)
# Let's see what we have now
print(crs.to_proj4())

#x=np.array(dset.variables['x'][:])
#y=np.array(dset.variables['y'][:])

x = np.arange(1, 3, 1)
y = np.arange(1, 3, 1)

xv,  yv = np.meshgrid(x, y)
print(xv)
print(yv)
conv = 0.3048
p = pyproj.Proj('+proj=tmerc +lat_0=0 +lon_0=9 +k=0.9996 +x_0=1500000 +y_0=0 +ellps=intl +units=m +no_defs')
lons, lats = p(xv*conv, yv*conv, inverse=True)

print(lons)
print(lats)
