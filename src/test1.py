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

dataSource = driver.Open(fileName, 0) # 0 means read-only. 1 means writeable.
print("Number of layers %d" % dataSource.GetLayerCount())

# getall features of the layer
# print coordinates of all lights
#layer = dataSource.GetLayer()
layer = dataSource.GetLayerByName('LIGHTS')
print("Layer: %s" % layer.GetName())
print("features %d" % layer.GetFeatureCount())

# getall features of the layer
for feature in layer:
    print dir(feature.DumpReadable())

defns = layer.GetLayerDefn()
print(dir(defns))
fieldCount = defns.GetFieldCount()
print("fields %d" % fieldCount)

for field in range(0,fieldCount):
    defn = defns.GetFieldDefn(field)
    print(defn)

for feature in layer:
    geom = feature.GetGeometryRef()
    #print(geom)
    #print geom.Centroid().ExportToWkt()



layer.ResetReading()
