# Download page from fuelwatch, parse for fuel costs
import feedparser
import sqlite3
import sys, os

base_url = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Suburb=%s&Surrounding=yes'

def find_suburb(postcode=None):
    if postcode is None:
        postcode = 6000
    
    # SQLite connection, get thingy
    con = sqlite3.Connection('./postcodes.sqlite')
    cur = con.cursor()
    
    cur.execute("SELECT postcode, locality FROM postcodes WHERE postcode = ?", (postcode,))
    
    pc = cur.fetchone()
    
    print "Returning {0} for postcode {1}".format(pc[1], pc[0])
    
    return {
        "postcode": pc[0],
        "suburb": pc[1],
    }

def fetch(suburb=None):
    
    #http://stackoverflow.com/questions/2299454/how-do-quickly-search-through-a-csv-file-in-python
    
    if suburb is None:
        suburb = "Perth"
    else:
        suburb = suburb['suburb']
    
    f = feedparser.parse(base_url % suburb)
    
    print "Fetching %s" % (base_url % suburb)
    
    result = []
    
    # if !entries, find next suburb or something like that iunno

    for entry in f.entries:
        
        relevant = {
            'price': entry['price'],
            'updated': entry['updated'],
            'location': entry['location'],
            'brand': entry['brand'],
            'coords': [entry['latitude'], entry['longitude']],
            'address': entry['address'],
        }
        
        result.append(relevant)
        
        #for k,v in relevant.iteritems():
        #    print "\t" + k + ": " + str(v)
            
    return result

if __name__ == "__main__":
    pc = sys.argv[1]
    print find_suburb(pc)
