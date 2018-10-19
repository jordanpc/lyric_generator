# import dependencies
import numpy as np
import datetime
import requests
from pprint import pprint
import pandas as pd
import os
import json

API_KEY = '395ba12d921dee55ad263b4c8b53dfc7'

# define a function to generate the closest saturday of our desired date
def getsaturday(date):
    "@date: given date, in format '2013-05-25'"
    d1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    t = datetime.timedelta((7 + 5 - d1.weekday()) % 7) # 5 is saturday
    next_saturday = d1 + t
    return next_saturday

# function to calculate the range for the for loop to generate list
def getdaterange(startdate, lastdate):
    "@startdate & lastdate: given date, in format '2013-05-25'"
    d1 = getsaturday(startdate)
    d2 = datetime.datetime.strptime(lastdate,'%Y-%m-%d')
    date_range = (d2 - d1).days/7
    return int(date_range)+1

def getdatelist(startdate, lastdate):
    "@startdate & lastdate: given date, in format '2013-05-25'"
    "@generate a list of saturday between the date range"
    # Create a list to store all saturdays
    date_list = []
    #date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    #date2 = datetime.datetime.strptime(last_date, '%Y-%m-%d')
    d1 = getsaturday(start_date)
    d2 = getsaturday(last_date)
    n = getdaterange(start_date, last_date)
    aweekago = datetime.timedelta(days=7)
    date_list.append(d2)
    date = d2 # define date as the last saturday of the datelist
    for i in range(n):
        new_date = date - aweekago
        date_list.append(new_date)
        date = new_date
    return date_list

def gettracksinfo(mbid):
    url = 'http://ws.audioscrobbler.com/2.0/'
    tracksinfo_url = f'{url}?method=track.getInfo&api_key={API_KEY}&mbid={mbid}&format=json'
    response = requests.get(tracksinfo_url)
    data = response.json()
    listeners = data['track']['listeners']
    playcount = data['track']['playcount']
    date = data['track']['wiki']['published']
    return (listeners, playcount, date)

def gettoptracks(pages):
    # Create a dataframe
    columns = ['rank','artist_name','song_title','genres']
    df = pd.DataFrame(columns=columns)
    # define key variables
    url = 'http://ws.audioscrobbler.com/2.0/'
    tag_name = 'pop'
    for page in range(pages):
        tracksbytag_url = f'{url}?method=tag.gettoptracks&tag={tag_name}&api_key={API_KEY}&format=json&page={page}'
        response_tracks = requests.get(tracksbytag_url)
        data = response_tracks.json()
        tracks = data['tracks']['track']
        for track in tracks:
            try:
                genres = tag_name
                rank = track['@attr']['rank']
                artist_name = track['artist']['name']
                song_name = track['name']
                duration = track['duration']
                mbid = track['mbid']
                track_info = gettracksinfo(mbid)
                listeners = track_info[0]
                playcount = track_info[1]
                date = track_info[2]
            except KeyError:
                rank = 'Not Available'
                artist_name = 'Not Available'
                song_name = 'Not Available'
            df = df.append({'rank':rank,
                            'artist_name':artist_name,
                            'song_title':song_name,
                            'genres':genres,
                            'duration':duration,
                            'listeners':listeners,
                            'playcount':playcount,
                            'date':date}, ignore_index=True)
    return df

# use last.fm API to generate a list of tags
def gettoptags():
    url = 'http://ws.audioscrobbler.com/2.0/'
    tags_url = f'{url}?method=chart.gettoptags&api_key={API_KEY}&format=json'
    response = requests.get(tags_url)
    tags_df = pd.DataFrame(response.json()['tags']['tag'])
    tags_df = tags_df.drop(columns=['streamable','wiki','url'])
    tags_df['reach'] = pd.to_numeric(tags_df['reach'], errors='raise', downcast='integer')
    tags_df = tags_df.sort_values(by=['reach'],ascending=False)
    tags_df = tags_df.set_index('name',drop=True)
    return tags_df 