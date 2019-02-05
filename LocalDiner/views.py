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


selected_venue_type = None

###### init ########

# unique_venue_cats = pd.read_sql_query('SELECT DISTINCT venue_cat_name FROM check_ins_table', con)['venue_cat_name']
# 
# 
# venues = pd.read_sql_query('SELECT * FROM venues_table', con)
# venues['score'] = np.random.rand(len(venues)) * 10
# venues = venues.sort_values('score', ascending=False)
# 

venues_details = pd.read_sql_query('SELECT id,name,phone,price,rating,score,lat,lon,url,cats FROM yelp_unique_venue_details', con)
unique_cats = list(set(', '.join(venues_details['cats'].unique()).split(', ')))


 


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
    venue_type = request.form.get('venue_type')
    venue_location = request.form.get('location') # not implemented yet
    venue_location = 'New York City'
    
    

    if (venue_type == None) or (venue_type == ''):
        venue_type = 'Pizza'

    venue_cats = [i for i in unique_cats if re.match('.*' + venue_type.lower() + '.*', i.lower())]

    venue_cats_text = venue_cats[0].lower() + ' places'

    cat_venues = pd.DataFrame(columns = venues_details.columns)
    for vc in venue_cats:
        cat_venues = pd.concat([cat_venues, venues_details[venues_details['cats'] == vc]])

    cat_venues = cat_venues.sort_values('score', ascending=False)




    num_hits = len(cat_venues)
    venues_longitude = cat_venues['lon'].values
    venues_latitude = cat_venues['lat'].values
    venue_loc = [venues_latitude.mean(), venues_longitude.mean()]

    all_coords = [] # initialize a list to store your addresses
    all_text = []

    for i in range(len(cat_venues)):
    
        name = cat_venues.iloc[i]['name']
        url = cat_venues.iloc[i]['url']
    #     address = cat_venues.iloc[i]['address']
        price = cat_venues.iloc[i]['price']
        rating = cat_venues.iloc[i]['rating']
        score = cat_venues.iloc[i]['score']
        fig = cat_venues.iloc[i]['id']
    

    return render_template('results.html', venue_loc = venue_loc, num_hits = num_hits, venue_cats = venue_cats_text, venue_location = venue_location, all_text = all_text, context=context)











@app.route('/api/coordinates', methods=['GET', 'POST']) 
def coordinates():

    global venue_cats
    global venue_type



    if (venue_type == None) or (venue_type == ''):
        venue_type = 'Pizza'

    venue_cats = [i for i in unique_cats if re.match('.*' + venue_type.lower() + '.*', i.lower())]

    venue_cats_text = venue_cats[0].lower() + ' places'

    cat_venues = pd.DataFrame(columns = venues_details.columns)
    for vc in venue_cats:
        cat_venues = pd.concat([cat_venues, venues_details[venues_details['cats'] == vc]])

    cat_venues = cat_venues.sort_values('score', ascending=False)




    num_hits = len(cat_venues)
    venues_longitude = cat_venues['lon'].values
    venues_latitude = cat_venues['lat'].values
    venue_loc = [venues_latitude.mean(), venues_longitude.mean()]

    all_coords = [] # initialize a list to store your addresses

    for i in range(len(cat_venues)):
    
        name = cat_venues.iloc[i]['name']
        url = cat_venues.iloc[i]['url']
    #     address = cat_venues.iloc[i]['address']
        price = cat_venues.iloc[i]['price']
        rating = cat_venues.iloc[i]['rating']
        score = cat_venues.iloc[i]['score']
    
    
        text = "<h4>" + "{:2.1f}".format(score) + '/10</h4><a href="' + url + '"><h3>' + name + "</h3></a>&emsp;" + price + "&emsp;&emsp;" + str(rating) + ' stars'

        address_details = {
        "lat": cat_venues.iloc[i]['lat'], 
        "lng": cat_venues.iloc[i]['lon'],
        "name": name,
        "text": text}
        all_coords.append(address_details)
    
    
    
    return jsonify({'coordinates': all_coords})









