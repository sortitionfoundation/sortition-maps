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

import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1kwgOpxMX4pwR3Myu4pXku4gjcnOS53bPOKwOGjZNxyI'
SAMPLE_RANGE_NAME = 'OECD!A1:BL'

os.environ["CARTOPY_USER_BACKGROUNDS"] = "background"

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


def make_map(data,year_to_plot):

    fig = plt.figure(figsize=(19.2, 10.8))
    ax = plt.axes(projection=ccrs.Mercator(central_longitude=0,
                                           min_latitude=-60,
                                           max_latitude=70))
    ax.background_img(name='BM', resolution='high')
    ax.set_extent([-170, 179, -60, 70], crs=ccrs.PlateCarree())

    years = []
    lats = []
    longs = []
    for row in data:
        try:
            if len(row) > 63 and float(row[12]) <= year_to_plot:
                years.append(float(row[12]))
                lats.append(float(row[62]))
                longs.append(float(row[63]))
        except:
            pass

    ax.scatter(longs, lats, color='#fd5734', transform=ccrs.PlateCarree())

    fontname = 'Open Sans'
    fontsize = 28
    # Positions for the date and grad counter
    date_x = -9
    date_y = -50
    # Date text
    ax.text(date_x, date_y,
            f"{year_to_plot:04d}",
            color='#fd5734',
            fontname=fontname, fontsize=fontsize * 1.3,
            transform=ccrs.PlateCarree())
    # Expands image to fill the figure and cut off margins
    fig.tight_layout(pad=-0.5)

    fig.savefig(f"frames/{year_to_plot:04d}.png", dpi=100,
                frameon=False, facecolor='black')
    ax.clear()



if __name__ == '__main__':
    data = get_data()
    for year in range(1990,2021):
        make_map(data,year)
