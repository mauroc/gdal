# http://www.gdal.org/drv_s57.html
# http://gdal.org/python/osgeo.ogr.Layer-class.html#GetLayerDefn
# https://pcjericks.github.io/py-gdalogr-cookbook/index.html

import os
from osgeo import ogr

try:
  from osgeo import ogr
  print 'Import of ogr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr from osgeo failed\n\n'

driverName = "S57"
driver = ogr.GetDriverByName( driverName )

fileName = 'US5WA13M/US5WA13M.000'
fileName = 'US5TX51M.000'
fileName = 'vector/CA/US5CA13M/US5CA13M.000'
#fileName = 'vector/CA/US5CA13M'

dataSource = driver.Open(fileName, 0) # 0 means read-only. 1 means writeable.
print("Number of layers %d" % dataSource.GetLayerCount())

for layer in dataSource:
    print(layer.GetName())

#layer = dataSource.GetLayer()
layer = dataSource.GetLayerByName('LIGHTS')
print("Layer: %s" % layer.GetName())
print("features %d" % layer.GetFeatureCount())

# getall features of the layer
for feature in layer:
    #print dir(feature.DumpReadable())
    geom = feature.GetGeometryRef()
    print("feature   ",feature.GetField("OBJNAM"))
    print(geom, geom.GetY(), geom.GetX())
    #print geom.Centroid().ExportToWkt()

# layer definition
l_defn = layer.GetLayerDefn()
print(dir(l_defn))
print("layer def name: %s" % l_defn.GetName())
fieldCount = l_defn.GetFieldCount()
print("fields %d" % fieldCount)


# field (attributes) definition
for field in range(0,fieldCount):
    a_defn = l_defn.GetFieldDefn(field)
    #print defn.DumpReadable()
    #print(dir(a_defn), a_defn.GetName(), a_defn.GetNameRef())


layer.ResetReading()
