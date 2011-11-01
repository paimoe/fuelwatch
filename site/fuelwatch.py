# Download page from fuelwatch, parse for fuel costs
import feedparser
import sqlite3
import sys

base_url = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Suburb=%s&Surrounding=yes'

def find_suburb(postcode=None):
    if postcode is None:
        postcode = 6000
    
    # SQLite connection, get thingy
    con = sqlite3.Connection('../postcodes.sqlite')
    cur = con.cursor()
    
    cur.execute("SELECT postcode, locality FROM postcodes WHERE postcode = ?", (postcode,))
    
    pc = cur.fetchone()
    
    return {
        "postcode": pc[0],
        "suburb": pc[1],
    }

def fetch(suburb=None):
    
    #http://stackoverflow.com/questions/2299454/how-do-quickly-search-through-a-csv-file-in-python
    
    if suburb is None:
        suburb = "Perth"
    
    f = feedparser.parse(base_url % suburb)
    
    result = []

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
