import csv
import sqlite3

con = sqlite3.Connection('../postcodes.sqlite')
cur = con.cursor()
cur.execute('CREATE TABLE "postcodes" (\
"postcode" varchar(4), \
"locality" varchar(200), \
"state" varchar(3), \
"comments" text, \
"delivery_office" varchar(200), \
"presort_indicator" varchar(20), \
"parcel_zone" varchar(20), \
"bsp_number" int, \
"bsp_name" varchar(200), \
"category" varchar(200));')

#"Pcode","Locality","State","Comments","DeliveryOffice","PresortIndicator","ParcelZone","BSPnumber","BSPname","Category"

f = open('./pc-book_20110905.csv')
csv_reader = csv.reader(f, delimiter=',')

cur.executemany('INSERT INTO postcodes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', csv_reader)
cur.close()
con.commit()
con.close()
f.close()

print "Done"
