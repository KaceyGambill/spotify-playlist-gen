import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# idk why I did it this way
uriList = []
tracks = []

# 1dpyjdum6LPLxP8qftIvtY
playlistID = "5uP5qd96U7DyVh0lzN6wnD"


# export SPOTIPY_CLIENT_ID='your-spotify-client-id'
# export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
# export SPOTIPY_REDIRECT_URI='your-app-redirect-url'


# oauth token can get from below link if lazy, make sure to add scope so that it
# can modify the playlist public/private
# https://developer.spotify.com/console/post-playlist-tracks/?playlist_id=&position=&uris=
auth = 'xxxxxxxxxxxxxxxxxxxxxxx'

spotify = spotipy.Spotify(auth=auth,client_credentials_manager=SpotifyClientCredentials())

# user added to spotify app
# https://developer.spotify.com/dashboard/applications
user = spotify.user('134817830')


# search list of artist
def search_list_artists():
    # testing an array before using a newline delimited file
    # artistList = ["marshmello", "timmy trumpet",] 
   
   # I never close this file, but oh well, I shoulda!
    with open("artist-list.bak") as file:
        artistList = file.readlines()
    print("ARTIST:")
    print(artistList)

    endpoint = "https://api.spotify.com/v1/search"
    headers = {
        "Content-Type": "application/json",
        # this is a different token then the 'auth' token above
        # this one was simple and not scoped to anything other than getting 
        # track's from artists
        # lazily got this from: https://developer.spotify.com/console/get-artist-top-tracks/?id=&market=
        "Authorization": "Bearer xxxxxxxxxxxxxxxxxxxx"
        }
    for artist in artistList:
        try:
            # query for artist
            # get only 1 artist per request
            payload = {
                    "q": artist,
                    "type": "artist",
                    "limit": "1"
                    }
            print(payload)

            r = requests.get(endpoint, params=payload, headers=headers)
            data = r.json()
            # cool data that is returned via the endpoint
            print(data['artists']['items'][0]['name'])
            print(data['artists']['items'][0]['uri'])
            print(data['artists']['items'][0]['popularity'])
            if(data['artists']['items'][0]['popularity'] < 40):
                uriList.append(data['artists']['items'][0]['uri'])
        except:
            # try/catch so that we don't crash on first error - there can be a few
            print("somethign went wrong")

# I should have returned the value, then used it later, but screw it
# used global tracks array
def get_top_tracks():
    for uri in uriList:
        results = spotify.artist_top_tracks(uri)
        # get the top 3 tracks, I would have thought it would have sliced the 
        # opposite way, but I think this was right from the small testing I did
        for track in results['tracks'][:3]:
            print(f"Track: {track['uri']}")
            tracks.append(track['uri'])

search_list_artists()
get_top_tracks()

def add_to_playlist(trackBite):
    print(f"track bite: {trackBite}")
    spotify.playlist_add_items(playlistID, trackBite)

def playlist_add():
    lengthOfTracks = len(tracks)
    # I was going to filter based do below logic if there are more then 100 tracks
    # decided to do below logic basically always...

    # spotify's API max's at 100 tracks per request though..

    if lengthOfTracks > 1:
        # weird tracks array splitting logic that actually worked
        print(f"Total number of tracks is: {lengthOfTracks}")
        chunkSmaller = lengthOfTracks  // 20
        # then we take the result of chunkSmaller and divide that by lengthOfTracks
        # that will give us our actual divisor, we run this 20 times, boom, 
        # maybe we are far out of our actual index, but the try/catch works great
        biteSize = lengthOfTracks // chunkSmaller

        print(tracks[:biteSize])
        x = range(20)
        for i in x:
            print(i)
            # print so we can see what the numbers look like because I never
            # trusted the logic
            print (f"bite would be {biteSize}{i}:{biteSize}*{i} +1")
            # careful with casing
            bitesize_one = biteSize*i
            bitesize_two = biteSize*(i+1)
            print(f"bitesize 1: {bitesize_one}")
            print(f"bitesize f: {bitesize_two}")
            trackBite = tracks[bitesize_one:bitesize_two]
            # if it's the the last group, idk why I put this in here it was super
            # late at this point
            try:
                if i == 19:
                    trackBite_minmusone = tracks[bitesize_one:bitesize_two-1]
                    add_to_playlist(trackBite_minusone)
                add_to_playlist(trackBite)
            except:
                print(f"""SOMETHING WENT WRONG WITH THE GROUP: {bitesize_one} and 
                        {bitesize_two}""")

playlist_add()


