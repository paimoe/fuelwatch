# Download page from fuelwatch, parse for fuel costs
import feedparser
import sqlite3
import sys, os

base_url = 'http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Suburb=%s&Surrounding=yes'

class NoDataException(Exception):
    def __init__(self, value="0000"):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
        
class NoSuburbException(Exception):
    pass

def find_suburb(postcode=None):
    if postcode is None:
        postcode = 6000
    
    # SQLite connection, get thingy
    con = sqlite3.Connection('./postcodes.sqlite')
    cur = con.cursor()
    
    cur.execute("SELECT postcode, locality FROM postcodes WHERE postcode = ?", (postcode,))
    
    pc = cur.fetchall()
    
    # pc is list of tuples(postcode, locality)
    # locality is what we pass to rss
    
    #for i in pc:
    #    print "Returning {0} for postcode {1}".format(i[1], i[0])
        
    return pc

def fetch(suburb=None):
    
    #http://stackoverflow.com/questions/2299454/how-do-quickly-search-through-a-csv-file-in-python
    if len(suburb) == 0:
        raise NoSuburbException()
    using_postcode = suburb[0][0]
    
    if suburb is None:
        suburb = iter([(6000, "Perth")])
    else:
        suburb = iter(suburb)
    
    results = []
    while len(results) == 0:
        try:
            where = suburb.next()
            
            f = feedparser.parse(base_url % where[1])
            
            if len(f.entries) > 0:
                results = f.entries
                using = where
        except StopIteration:
            # Cheese it
            raise NoDataException(using_postcode)
    
    result = []
    i = 0
    for entry in results:
        
        relevant = {
            'id': i,
            'price': entry['price'],
            'updated': entry['updated'],
            'location': entry['location'].strip().title(),
            'brand': entry['brand'],
            'coords': [entry['latitude'], entry['longitude']],
            'address': entry['address'],
        }
        
        result.append(relevant)
        
        i += 1
        #for k,v in relevant.iteritems():
        #    print "\t" + k + ": " + str(v)
            
    return {
        "using": where[1],
        "postcode": where[0],
        "results": result
    }

if __name__ == "__main__":
    pc = sys.argv[1]
    s2 = find_suburb(pc)
    s = fetch(s2)
    print "Using: %s" % s['using']
    print "Postcode: %s" % s['postcode']
    print s['results'][0]
