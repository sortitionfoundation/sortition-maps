#!/usr/bin/env python3
""" Script to add longitude and latitude columns to CSV file containing OECD
    database of deliberative democracies.

    Created by David Western, June 2020
"""

import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from numpy.random import rand
import ssl
import certifi
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

fileIn = 'OECD.csv'
fileOut = 'OECD2.csv'

cityCol = 'Place (Country/State/Region/City)'
countryCol = 'Country'

# Read data from file:
df = pd.read_csv(fileIn)
df['place'] = df[cityCol]+", "+df[countryCol]

# Get lat/lng data using geopy
locator = geopy.geocoders.Nominatim(user_agent='myGeocoder')
locations = df['place'].apply(locator.geocode)
points = locations.apply(lambda loc: tuple(loc.point) if loc else None)
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(points.tolist(), index=df.index)
# df['latitude'] = rand(len(df),1)
# df['longitude'] = rand(len(df),1)

# Modify duplicates
df['dup'] = df.duplicated(subset=['latitude','longitude'],keep='first')
df['offset'] = (rand(len(df),1)-0.5)*0.01
df['latitude'] = [l+o if d else l for l,o,d in zip(df['latitude'],df['offset'],df['dup'])]
df['longitude'] = [l+o if d else l for l,o,d in zip(df['longitude'],df['offset'],df['dup'])]

# Clean up - delete unwanted new columns
df = df.drop(columns=['place','altitude','offset','dup'])

# Save to file
df.to_csv(fileOut,index=False)
