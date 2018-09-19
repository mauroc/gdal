
# without SQLAlchemy --------------------------
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="P0nte_di_legn0", db="bbxais_development" )
cur=db.cursor()
cur.execute("SELECT * FROM vessels")

# print entire result set
print cur.fetchall()

# print all IDs of records
for row in cur.fetchall():
    print row[0]

# see here to insert records into tables https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

db.close()


# using SQLAlchemy ORM model -----------------------------

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# need to do more research on how to connect to an existing mysql dabase. most of the tutorials I have seen use sqlite.....
 
