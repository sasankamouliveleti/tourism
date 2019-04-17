import yaml
import requests
import datetime
import time
import csv
import json
# Get all Venue IDs for venues within the bounding box.


def get_delta(lower, upper, length):
    return (upper - lower)/length


with open("config.yaml", "r") as f:
    cfg = yaml.load(f)

lat_delta = get_delta(cfg['top_bound'], cfg['bottom_bound'], cfg['grid_size'])
long_delta = get_delta(cfg['left_bound'], cfg['right_bound'], cfg['grid_size'])

search_params = {
    'client_id': cfg['client_id'],
    'client_secret': cfg['client_secret'],
    'intent': 'browse',
    'limit': 50,
    'v': '20180218'
}

venue_ids = set()
search_count = 0
i=0
for lat in range(cfg['grid_size']):
    for long in range(cfg['grid_size']):
        ne_lat = cfg['top_bound'] + lat * lat_delta
        ne_long = cfg['left_bound'] + (long+1) * long_delta

        search_params.update({'ne': '{},{}'.format(ne_lat, ne_long),
                              'sw': '{},{}'.format(ne_lat + lat_delta,
                                                   ne_long - long_delta)})

        r = requests.get('https://api.foursquare.com/v2/venues/search',
                         params=search_params)
		
        if 'venues' in r.json()['response']:
            venues = r.json()['response']['venues']
            #y = 'data'+str(i)+'.json'
            with open('merged.json','a') as f:
                json.dump(venues,f)
            #i=i+1
			
		
			

            #for venue in venues:
               # venue_ids.add(venue['id'])

        #search_count += 1

        
        # gets fussy when more than 5000 requests/hr

