import os
import csv
from osgeo import ogr
import MySQLdb
import datetime
import json

try:
    from osgeo import ogr
    print 'Import of ogr from osgeo worked.  Hurray!\n'
except:
    print 'Import of ogr from osgeo failed\n\n'

def parse_chart(file_name,chart_name):
    global chart_count, driver, tot_objs, s57classes, dups
    print "\n" , file_name
    chart_count+=1
    dups = 0
    dataSource = driver.Open(file_name, 0) # 0 means read-only. 1 means writeable.
    for s57class in s57classes:
        layer = dataSource.GetLayerByName(s57class)
        if layer:
            num_objs = layer.GetFeatureCount()
            tot_objs += num_objs
            for feature in layer:
                sql_create_obj(chart_name, s57class, feature)
    dataSource=None

def create_hash(s57class,feature):
    global s57classes
    data_hash={}
    if s57classes[s57class]:
        for attr_class in ['attra', 'attrb', 'attrc']:    
            #attrs = {}
            klasses=s57classes[s57class] and s57classes[s57class][attr_class] and s57classes[s57class][attr_class].split(';')
            if klasses:            
                for klass in klasses:
                    if klass:
                        try:
                            #todo classes with lower case names generate error
                            klass_value =feature.GetField(klass.upper())    
                        except:
                            klass_value = None
                            pass
                        if klass_value: 
                            #attrs[klass]=klass_value
                            data_hash[klass]=klass_value
                #data_hash[attr_class]= attrs
    return data_hash

def sql_find_obj(lnam,s57class):
    global db, cur
    # https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
    cur.execute("SELECT id FROM s57objs WHERE lnam = %s AND f_class = %s", (lnam, s57class) )
    return cur.fetchall()

def sql_create_obj(chart_name, s57class, feat):
    global db, cur, s57classes, tot_unique_objs,dups
        geom = feat.GetGeometryRef()
    if geom.GetDimension() > 0:  # 1 is line, 2 is polygon
        #todo decide how to manage lines and polygons. Right now we just save the centroid
        geom= geom.Centroid()
    #f_id = feat.GetFID()
    lnam = feat.GetField('LNAM')
    if sql_find_obj(lnam, s57class)!=():        
        dups+=1
        print("\rfeatures already in database: %s" % dups),
    else:
        tot_unique_objs += 1
        data_hash=create_hash(s57class,feat)
        longitude, latitude = geom.GetX(), geom.GetY()
        #https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
        #data_hash_s= str(data_hash).replace("\'","\"")
        data_hash_s = json.dumps(data_hash, encoding='latin1')
        add_obj = ("INSERT INTO s57objs ( f_class, lnam, latitude, longitude,chart_name, tags, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        cur.execute(add_obj, (s57class, lnam, latitude, longitude, chart_name, data_hash_s, datetime.datetime.now(), datetime.datetime.now() ) )
        db.commit()

def scan_charts():
    # walk the entire chart directory and process files with extension '.000'
    for root, dirs, files in os.walk(root_dir):
        path = root.split(os.sep)
        for file in files:
        chart_name, file_extension = os.path.splitext(file)
        #print filename, file_extension
        if file_extension == '.000':
            file_name=root+"/"+file
            parse_chart(file_name,chart_name)
    print("Charts scanned: %s. S57 objects found: %s. SQ Unique objs added: %s " % (chart_count, tot_objs, tot_unique_objs))

# ==================================================================================    
# initialize variables
root_dir = '/root/ENC_ROOT'
driverName = "S57"
driver = ogr.GetDriverByName( driverName )
chart_count = tot_objs = tot_unique_objs = dups = 0
db = MySQLdb.connect(host="localhost", user="root", passwd="P0nte_di_legn0", db="bbxais_development" )
cur=db.cursor()

# import s57 classes managed by squiddio and load them in a hash
s57classes = {}
with open('s57sqclasses.csv') as csvfile:
    classes=csv.reader(csvfile)
    for row in classes:
        if row[0]=='*':
            s57classes[row[3]]={'code': row[1], 'objclass': row[2],'attra': row[4],'attrb': row[5],'attrc': row[6],'class': row[7],\
            'primitives': row[8]}

#set test vars
#path_name = '/root/ENC_ROOT/US5CA93M/US5CA93M.000'
#chart_name="US5CA93M"
#parse_chart(path_name,chart_name)

scan_charts()

cur.close

