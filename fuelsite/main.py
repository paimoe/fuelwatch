# Yeah go Flask
from flask import Flask
from flask import render_template, url_for, request, abort, make_response

import feedparser
import requests
import json
import sys,os

import fuelwatch as fw

app = Flask(__name__)

#DEBUG = 'local' in sys.argv    

@app.route("/ajax/<t>", methods=['POST'])
def ajax(t):
    if t == 'dataset':
        # Is sent a postcode... then figures out the suburb
        # Returns a template of dataset_table.html, which is then dynamically loaded
        postcode = request.form['postcode']
        suburb = fw.find_suburb(postcode)
        data = fw.fetch(suburb) # Should be result
        response = make_response(render_template('dataset_table.html', prices=data['results']))
        response.headers['X-Perthfuel-Suburb'] = data['using']
        return response
    abort(403)
    
@app.route("/fetch")
def fetch():
    # u = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + this.position + '&sensor=false'
    data = {"result": 'error', "message": ''}
    coords = request.args.get('coords', False)
    postcode = request.args.get('postcode', False)
    
    if postcode:
        return json.dumps({'message': postcode, 'result': 'OK'})
    
    if not coords:
        data['message'] = 'Coordinates not found'
        return json.dumps(data) 
        
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?sensor=false&latlng=' + coords)
    if r.status_code != 200:
        data['message'] = 'Incorrect response from Maps: %s' % r.status_code
        return json.dumps(data) 
        
    j = json.loads(r.content)
    
    # Fuck it just loop it, its like 5 things
    wanted = None
    for result in j['results']:
        if result['types'][0] == 'postal_code':
            wanted = result
            
    if wanted is None:
        data['message'] = 'Could not find post_code in json response'
        return json.dumps(data) 
        
    # result hasss.. the post code
    postcode = wanted['address_components'][0]['long_name']
    print "POSTCODE IS " + postcode
    
    data['result'] = 'OK'
    data['message'] = postcode
    return json.dumps(data) # return json object

@app.route("/<int:postcode>")
@app.route("/")
def hello(postcode=None):
    
    # This should then launch the JS
    if postcode is None or len(str(postcode)) != 4:
        msg = "Default"
        return render_template('index.html', msg="Default")
        
    else:
        pc = postcode
        denyJS = True
        
        # Get all pricing information, format, and send to browser
        suburb = fw.find_suburb(pc)
        all = fw.fetch(suburb)
        
        return render_template('index.html', pc=postcode, denyJS=True, prices=all['results'], suburb_used=all['using'])
    return render_template('index.html')


if __name__ == "__main__":
    if 'local' in sys.argv:
        
        app.run(debug=True)
    else:
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
