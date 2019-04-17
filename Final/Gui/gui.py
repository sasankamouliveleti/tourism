from tkinter import *
import json
import pandas as pd
from nltk.probability import *
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from geopy.geocoders import Nominatim
import yaml
import requests
import datetime
import time
import csv
import ctypes


top =Tk()
top.geometry("1000x200")
top.title("Data Visualisation")

def mangle(s):
    return s.strip()[1:-1]

def cat_json(output_filename, input_filenames):
    with open(output_filename, "w") as outfile:
        first = True
        for infile_name in input_filenames:
            with open(infile_name) as infile:
                if first:
                    outfile.write('[')
                    first = False
                else:
                    outfile.write(',')
                outfile.write(mangle(infile.read()))
        outfile.write(']')

def get_delta(lower, upper, length):
    return (upper - lower)/length

def datafinder():
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    loc=E1.get()
    location = geolocator.geocode(str(loc))
    print(location.latitude, location.longitude)
    top_bound= location.latitude-0.99
    bottom_bound = location.latitude+0.99
    right_bound = location.longitude+0.99
    left_bound = location.longitude-0.99
    grid_size= 100
    lat_delta = get_delta(top_bound, bottom_bound, grid_size)
    long_delta = get_delta(left_bound, right_bound, grid_size)

    search_params = {
        'client_id': 'KMY0MACFH2LRFJJEPWNJYKBOFIXQSNFTFUFX523HBAG3YHES',
        'client_secret': '2VS5FAEAQCGWYZUPSXLO225W1XG33NK3IC3EKLFTUZF1PWAG',
        'intent': 'browse',
        'limit': 50,
        'v': '20180218'
    }

    venue_ids = set()
    search_count = 0
    i = 0

    for lat in range(grid_size):
        if(i>=10):
            break
        for long in range(grid_size):
            if(i>=10):
                break
            ne_lat = top_bound + lat * lat_delta
            ne_long = left_bound + (long + 1) * long_delta

            search_params.update({'ne': '{},{}'.format(ne_lat, ne_long),
                                  'sw': '{},{}'.format(ne_lat + lat_delta,
                                                       ne_long - long_delta)})

            r = requests.get('https://api.foursquare.com/v2/venues/search',
                             params=search_params)

            if 'venues' in r.json()['response']:
                venues = r.json()['response']['venues']
                if(len(venues)==0):
                    continue

                y = 'data'+str(i)+'.json'
                with open(y, 'w') as f:
                    json.dump(venues, f)
                i=i+1
    k=i
    print("done loading data please proceed ")





    outputfilename = 'output.json'
    input_filenames = []
    for i in range(k):
        input_filenames.append('data' + str(i) + '.json')
    cat_json(outputfilename, input_filenames)



def foresquare():
    with open("output.json", "r") as f:
        elevations = json.load(f)
        print("its working")
    df = pd.DataFrame(elevations)
    length=df.shape[0]
    category = []
    for i in range(length):
        if (len(df['categories'][i]) != 0):
            category.append(df['categories'][i][0]['name'])

    df['lat'] = df['location'].apply(lambda col: col['lat'])  # arrrrgh
    df['lon'] = df['location'].apply(lambda col: col['lng'])
    latitude = df['lat'].tolist()
    longitude = df['lon'].tolist()
    fd_1 = FreqDist(category)
    catego = set(category)
    print(len(catego))
    print(fd_1.most_common(10))
    '''post = []
    postlat = []
    postlon = []
    park = []
    parklat = []
    parklon = []
    cafe = []

    cafelat = []
    cafelon = []
    for i in range(len(category)):
        if (category[i] == 'Post Office'):
            post.append(i)
        elif (category[i] == 'Park'):
            park.append(i)
        elif (category[i] == 'Café'):
            cafe.append(i)

    for i in range(len(post)):
        postlat.append(latitude[post[i]])
        postlon.append(longitude[post[i]])
    for i in range(len(park)):
        parklat.append(latitude[park[i]])
        parklon.append(longitude[park[i]])
    for i in range(len(cafe)):
        cafelat.append(latitude[cafe[i]])
        cafelon.append(longitude[cafe[i]])'''
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    loc = E1.get()
    location = geolocator.geocode(str(loc))
    output_file("gmap.html")

    map_options = GMapOptions(lat=location.latitude, lng=location.longitude, map_type="roadmap", zoom=8)

    p = gmap("AIzaSyDvrQNLU4NALrtXE4StvhzMiWbdUIfN7vk", map_options, title="Melbourne")

    source = ColumnDataSource(
        data=dict(lat=latitude,
                  lon=longitude)
    )
    '''source1 = ColumnDataSource(
        data=dict(lat1=parklat,
                  lon1=parklon)
    )
    source2 = ColumnDataSource(
        data=dict(lat2=postlat,
                  lon2=postlon)
    )'''
    p.circle(x="lon", y="lat", size=5, fill_color="blue", fill_alpha=0.8, source=source)
    #p.circle(x="lon1", y="lat1", size=5, fill_color="green", fill_alpha=0.8, source=source1)
    #p.circle(x="lon2", y="lat2", size=5, fill_color="red", fill_alpha=0.8, source=source2)
    print("its working")
    show(p)
def datafinder1():
    print("you are there")
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    loc = E1.get()
    location = geolocator.geocode(str(loc))
    print(location.latitude, location.longitude)
    top_bound = location.latitude - 0.99
    bottom_bound = location.latitude + 0.99
    right_bound = location.longitude + 0.99
    left_bound = location.longitude - 0.99
    grid_size = 100
    lat_delta = get_delta(top_bound, bottom_bound, grid_size)
    long_delta = get_delta(left_bound, right_bound, grid_size)
    API_KEY = 'DRtXPE0LNvt9mgsaWdgZVQFzl98a-5NxB2vEBQS5tIZGWR3Sr3F_U08A-RCOOAJgzgxbT_ZDGQOsWNaXESCQw2MguK-hybOJPcFEpt_c3cXDI8WbKUHPQVGseGCQXHYx'
    HEADERS = {'Authorization': 'bearer %s' % API_KEY}
    search_params = {
        'limit': 50,
        'location': str(loc)

    }

    venue_ids = set()
    search_count = 0
    i = 0
    for lat in range(grid_size):
        if(i>=10):
            break
        for long in range(grid_size):
            if(i>=10):
                break
            ne_lat = top_bound + lat * lat_delta
            ne_long =left_bound + (long + 1) * long_delta

            search_params.update({'latitude': '{}'.format(ne_lat),
                                  'longitude': '{}'.format(ne_long - long_delta)})

            r = requests.get('https://api.yelp.com/v3/businesses/search',
                             params=search_params, headers=HEADERS)

            # if 'venues' in r.json()['response']:
            #    venues = r.json()['response']['venues']
            y = 'data' + str(i) + '.json'
            venues = r.json()
            with open(y, 'w') as f:
                json.dump(venues, f)
            i = i + 1
    k=i
    for i in range(2,k):
        x = 'data' + str(i) + '.json'
        y = 'da' + str(i) + '.json'
        with open(x, "r") as f:
            elevation = json.load(f)
        with open(y, "w") as f:
            json.dump(elevation['businesses'], f)
    outputfilename = 'output1.json'
    input_filenames = []
    for i in range(2, k):
        input_filenames.append('da' + str(i) + '.json')
    print(input_filenames)
    cat_json(outputfilename, input_filenames)
    print("done thing")
    ctypes.windll.user32.MessageBoxW(0, "Data Loading Done", "Done", 1)

def yelp():
    with open("output1.json", "r") as f:
        elevation = json.load(f)
    df = pd.DataFrame(elevation)
    df['lat'] = df['coordinates'].apply(lambda col: col['latitude'])  # arrrrgh
    df['lon'] = df['coordinates'].apply(lambda col: col['longitude'])
    latitude = df['lat'].tolist()
    longitude = df['lon'].tolist()
    revcount = df['review_count'].tolist()
    print(max(revcount))
    category = []
    length = df.shape[0]
    for i in range(length):
        if (len(df['categories'][i]) != 0):
            category.append(df['categories'][i][0]['title'])
    fd_1 = FreqDist(category)
    print(fd_1.most_common(10))
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    loc = E1.get()
    location = geolocator.geocode(str(loc))
    output_file("gmap.html")

    map_options = GMapOptions(lat=location.latitude, lng=location.longitude, map_type="roadmap", zoom=8)
    p = gmap("AIzaSyDvrQNLU4NALrtXE4StvhzMiWbdUIfN7vk", map_options, title="Melbourne")

    source = ColumnDataSource(
        data=dict(lat=latitude,
                  lon=longitude)
    )

    p.circle(x="lon", y="lat", size=5, fill_color="blue", fill_alpha=0.8, source=source)

    show(p)
    print("completed")
frame=Frame(top)
frame.pack()
B = Button(frame, text ="Foresquare", command = foresquare)
B1 = Button(frame, text ="Yelp", command = yelp)
B.pack(padx=50,pady=50,side= LEFT)
B1.pack(padx=50,pady=50,side= LEFT)
L1 = Label(frame, text="Location")
L1.pack(padx=50,pady=50,side = LEFT)
E1 = Entry(frame, bd =5)
E1.pack(side = LEFT)

dataval=Button(frame, text='dataforesquare', command=datafinder)
dataval.pack(padx=50,pady=50,side = LEFT)
dataval=Button(frame, text='datayelp', command=datafinder1)
dataval.pack(padx=50,pady=50,side = LEFT)


top.mainloop()
