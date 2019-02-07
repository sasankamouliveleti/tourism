import yaml
import requests
import datetime
import time

def get(lower, upper, length):
    return (upper - lower)/length


with open("config.yaml", "r") as f:
    y= yaml.load(f)

lat_delta = get(y['top'], y['bottom'], y['grid'])
long_delta = get(y['left'], y['right'], y['grid'])

search_params = {
    'client_id': y['client_id'],
    'client_secret': y['client_secret'],
    'intent': 'browse',
    'limit': 50,
    'v': '20180218'
}

venue_ids = set()
search_count = 0
fh= open("data.txt","w")
for lat in range(y['grid']):
    for long in range(cfg['grid']):
        ne_lat = y['top'] + lat * lat_delta
        ne_long = y['left'] + (long+1) * long_delta

        search_params.update({'ne': '{},{}'.format(ne_lat, ne_long),
                              'sw': '{},{}'.format(ne_lat + lat_delta,
                                                   ne_long - long_delta)})

        r = requests.get('https://api.foursquare.com/v2/venues/search',
                         params=search_params)

        if 'venues' in r.json()['response']:
            venues = r.json()['response']['venues']
            print(venues)
            fh.write(str(venues))

            for venue in venues:
                venue_ids.add(venue['id'])


        search_count += 1


