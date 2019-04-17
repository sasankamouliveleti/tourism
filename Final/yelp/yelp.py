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

e
			
		
			

        #    for venue in venues:
         #       venue_ids.add(venue['id'])

        #search_count += 1

        
        # gets fussy when more than 5000 requests/hr
        #if search_count % 5000 == 0:
         #   time.sleep(60*60)

        #time.sleep(0.1)

