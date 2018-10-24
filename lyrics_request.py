import requests
from bs4 import BeautifulSoup
from lastfm_api import gettoptracks
import numpy as np
import datetime
from pprint import pprint
import pandas as pd
import os
import json

# api key for last.fm
API_KEY = '395ba12d921dee55ad263b4c8b53dfc7'

BEARER_TOKEN = "hLLUI0D7QaKVaulNUbThPLC_JDjr9c3BrufGEcyw6C9FpW4YDNqHc1NOgaBspgkW"
client_id = "ts8I1lK-3eAlvDw33cI2PbWYVXa9pE4Q2aSUeIWcWSei02MKLYkkL4F-Q7F1U6Id"
client_access = "QchBo2tCBes7AWgA7LNJLQ0LvG_HV5Py6qj3nZ2YgsmumzCUqcGWY8BCt7rL6psr"

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer hLLUI0D7QaKVaulNUbThPLC_JDjr9c3BrufGEcyw6C9FpW4YDNqHc1NOgaBspgkW'}

#function to run API request and HTML parsing
def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find("div", class_= "lyrics").get_text() 
    return lyrics

# generate 100*50 = 5,000 tracks with the gettoptrack function
tracks = gettoptracks(100,'pop')
tracks['api_path'] = ""
print(f'the total # of tracks is {len(tracks)}')

counter = 0
for i,row in tracks.iterrows():
    song_title = row['song_title']
    artist_name = row['artist_name']
    base_url = "http://api.genius.com"
    url = f'{base_url}/search'
    params = {'q': song_title}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    api_path = None
    hits_list = data['response']['hits']
    for item in hits_list:
        name = item['result']['primary_artist']['name']
        if name == artist_name:
            api_path = item['result']['api_path']
            tracks.loc[i,'api_path'] = api_path
            counter =+ 1
            if (counter % 5000 == 0) and (counter > 0):
                tracks.to_csv(f'output_{counter/1000}k_nolyrics.csv')
            break
    if api_path is None:
        tracks.loc[i,'api_path'] = "Not Available"

counter_1 = 1
tracks['lyrics'] = ''
for i,row in tracks.iterrows():
    api_path = row['api_path']
    base_url = "http://api.genius.com"
    if api_path == 'Not Available':
        tracks.loc[i,'lyrics'] = 'Not Available'
    else:
        lyrics = lyrics_from_song_api_path(api_path)
        tracks.loc[i,'lyrics'] = lyrics
        if (counter % 5000 == 0) and (counter > 0):
            tracks.to_csv(f'output_{counter/1000}_withlyrics.csv')
tracks.to_csv('output_withlyrics_final.csv')