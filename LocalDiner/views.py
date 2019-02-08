from LocalDiner import app

from flask import render_template, request, jsonify
from flask_googlemaps import GoogleMaps, Map

import re, os
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

dbname = 'FourSquare'
username = 'mari' # change this to your username

engine = create_engine('postgres://%s@localhost/%s'%(username,dbname))

con = None
con = psycopg2.connect(database = dbname, user = username)


GoogleMaps(app)


venues = pd.read_sql_query('SELECT * FROM venues', con)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
        
        

@app.route('/results', methods=['GET', 'POST'])
def results():

    context = {
            "key": app.config['GOOGLEMAPS_KEY']
        }



    global venue_cats
    global venue_type
    global venues_in_cat
    
    venue_type = request.form.get('venue_type')
    venue_location = request.form.get('location') # not implemented yet
    venue_location = 'New York City'

    
    

    if (venue_type == None) or (venue_type == ''):
        venue_type = 'Pizza'
    if (venue_location == None) or (venue_location == ''):
        venue_location = 'New York City'
        
    venue_type = venue_type.split(' ')[0]
    venue_type_text = venue_type.lower() + ' places'

    inds = [n for n,i in enumerate(venues['cats']) if re.match('.*' + venue_type.lower() + '.*', i.lower())]
    venues_in_cat = venues.loc[inds].sort_values('prediction',
                                                 ascending = False)



    num_hits = len(venues_in_cat)
    venues_longitude = venues_in_cat['lon'].values
    venues_latitude = venues_in_cat['lat'].values
    venue_loc = [venues_latitude.mean(), venues_longitude.mean()]

    

    return render_template('results.html', venue_loc = venue_loc, num_hits = num_hits, venue_cats = venue_type_text, venue_location = venue_location, context = context)











@app.route('/api/coordinates', methods=['GET', 'POST']) 
def coordinates():

    global venue_cats
    global venue_type
    global venues_in_cat


 
    all_venue_info = [] # initialize a list to store your addresses

    for i in range(len(venues_in_cat)):
    
        item = {

        "name" : venues_in_cat.iloc[i]['name'],
        "url" : venues_in_cat.iloc[i]['url'],
        "address" : venues_in_cat.iloc[i]['clean_address'],
        "price" : venues_in_cat.iloc[i]['price'],
        "rating" : venues_in_cat.iloc[i]['rating'],
        "score" : venues_in_cat.iloc[i]['prediction'],
        "venue_id" : venues_in_cat.iloc[i]['id'],
        "lat": venues_in_cat.iloc[i]['lat'], 
        "lng": venues_in_cat.iloc[i]['lon'],
        
        }
        
        item["text"] =  "<h4>" + "{:2.1f}".format(item['score']) + '/10</h4><a href="' + item['url'] + '"><h3>' + item['name'] + "</h3></a>&emsp;" + str('$' * item['price']) + "&emsp;&emsp;" + str(item['rating']) + ' stars'

        
        
        
        all_venue_info.append(item)



    return jsonify({'coordinates': all_venue_info})




