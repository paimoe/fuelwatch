# Yeah go Flask
from flask import Flask
from flask import render_template, url_for, request

import feedparser
import requests
import json
import sys,os

app = Flask(__name__)

@app.route("/")
def hello(name=None):
	return render_template('index.html', name=name)
    
    
@app.route("/fetch")
def fetch():
    # u = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + this.position + '&sensor=false'
    coords = request.args.get('coords', False)
    if not coords:
        return 'error'
        
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?sensor=false&latlng=' + coords)
    if r.status_code != 200:
        return 'not 200 whattttt: %s' % r.status_code
        
    j = json.loads(r.content)
    
    # Fuck it just loop it, its like 5 things
    wanted = None
    for result in j['results']:
        if result['types'][0] == 'postal_code':
            wanted = result
            
    if wanted is None:
        return "FUCSLDjgB"
        
    # result hasss.. the post code
    postcode = wanted['address_components'][0]['long_name']
    #print wanted['address_components']
    #print "POSTCODE IS " + postcode
        
    return r.content



if __name__ == "__main__":
    if 'local' in sys.argv:
        app.run(debug=True)
    else:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
