""" Generate the frames for an animation showing sortition events accumulating around the globe
over recent years.

N.B. To run this script you will need to add your own credentials.json file to the working
directory. This file can be created in the Google Developer Console.

Created by David Western, Sep 2020.
"""


from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1kwgOpxMX4pwR3Myu4pXku4gjcnOS53bPOKwOGjZNxyI'
SAMPLE_RANGE_NAME = 'OECD!A1:BL'

os.environ["CARTOPY_USER_BACKGROUNDS"] = "background"

res = 'low'
dpi = {'high':100, 'low':50}

start_year = 1990
end_year = 2021

colour1 = '720046'
colour2 = 'fd5734'

def get_data():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    return values


def make_map(data, year_to_plot, fig):

    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,
                                           min_latitude=-60,
                                           max_latitude=70))
    ax.background_img(name='BG', resolution=res)
    ax.set_extent([-170, 179, -60, 70], crs=ccrs.PlateCarree())

    years = []
    lats = []
    longs = []
    colrs = np.empty((0,3))
    for row in data:
        try:
            if len(row) > 63 and float(row[12]) <= year_to_plot:
                year = float(row[12])
                years.append(year)
                colrs = np.append(colrs, year_to_colour(year), axis=0)
                lats.append(float(row[62]))
                longs.append(float(row[63]))
        except:
            pass

    alpha = 0.6
    rgba = np.ones((len(years), 4))*alpha
    rgba[:, :-1] = colrs
    ax.scatter(longs, lats, color=rgba, s=100, edgecolors='none', transform=ccrs.PlateCarree())

    fontname = 'Open Sans'
    fontsize = 28
    # Positions for the date and grad counter
    date_x = -9
    date_y = -50
    # Date text
    colr = year_to_colour(year_to_plot)
    colr = (colr[0][0], colr[0][1], colr[0][2])
    ax.text(date_x, date_y,
            f"{year_to_plot:04d}",
            color=colr,
            fontname=fontname, fontsize=fontsize * 1.3,
            transform=ccrs.PlateCarree())
    # Expands image to fill the figure and cut off margins
    # fig.tight_layout(pad=-0.5)

    fig.savefig(f"frames/{year_to_plot:04d}.png", dpi=dpi[res],
                facecolor='black')
    ax.clear()

def hex_to_rgb(hex):
    return np.array([[int(hex[i:i + 2], 16)/255 for i in (0, 2, 4)]])

def year_to_colour(year):
    rgb1 = hex_to_rgb(colour1)
    rgb2 = hex_to_rgb(colour2)
    year = max(year,start_year)
    return rgb1 + (year - start_year) / (end_year - start_year) * (rgb2 - rgb1)

def make_gif():
    from pathlib import Path
    from PIL import Image, ImageFilter

    # Load images
    images = []
    pathlist = Path('frames').glob('**/*.png')
    for path in pathlist:
        images.append(Image.open(path))
    # Repeat the last frame so it stays up a while
    for k in range(5):
        images.append(Image.open(path))
    # Save to gif file
    images[0].save('gifs/map.gif',
                   save_all=True, append_images=images[1:], optimize=True, duration=500, loop=0)


if __name__ == '__main__':
    data = get_data()
    fig = plt.figure(figsize=(19.2, 10.8))
    for year in range(start_year,end_year):
        make_map(data,year,fig)
    fig.close()
    make_gif()
