# Yeah go Flask
from flask import Flask
from flask import render_template, url_for, request

import feedparser
import requests

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
        
    return r.content

if __name__ == "__main__":
	app.run(debug=True)
