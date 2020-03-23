# import spotipy
# import spotipy.util as util

username = 'thunderbolt232'
scope = 'playlist-modify-public'

def searchURI(spotify, artist, song):
    searchQuery = 'artist:' + artist + ' track:' + song
    results = spotify.search(q=searchQuery, type='track')['tracks']['items']
    maxIndex = 0
    maxValue = -1
    for index in range(len(results)):
        result = results[index]
        value = 0
        result_name = result['name'].lower()
        remix = (('remix' in song) == ('remix' in result_name))
        vip = (('vip' in song) == ('vip' in result_name))
        type_matches = remix and vip
        album_type = result['album']['album_type']
        album_name = result['album']['name'].lower()
        album_artist = result['album']['artists'][0]['name'].lower()
        print(result['popularity'], album_type, album_artist)
        if type_matches:
            if album_artist == 'monstercat':
                if 'uncaged' in album_name or 'instinct' in album_name or 'monstercat 0' in album_name:
                    value = 3
            elif album_artist == artist:
                if album_type == 'album':
                    value = 2
                elif album_type == 'single':
                    value = 1
            else:
                value = 0
        if value > maxValue:
            maxValue = value
            maxIndex = index
    return results[maxIndex]['uri']
def getURIs(spotify, entries):
    URI = []
    for entry in entries:
        artist = entry[0].lower()
        song = entry[1].lower()
        URI += [searchURI(spotify, artist, song)]
    return URI
def addToPlaylistFromURI(spotify, playlist, URIs): #make sure song not already in playlist
    result = spotify.user_playlist(username, playlist, 'tracks')['tracks']['items']
    playlistURIs = []
    for uri in URIs:
        playlistURIs.append(uri)
    # for i in result:
    #     playlistURIs += [i['track']['uri']]
    # for uri in URIs:
    #     if uri in playlistURIs:
    #         playlistURIs.remove(uri)
    #     else:
    #         playlistURIs.append(uri)
    if len(playlistURIs) > 0:
        spotify.user_playlist_add_tracks(username, playlist, playlistURIs)

import spotipy
import spotipy.util as util
import pyodbc
import time
start = time.time()
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\thund\Python\Spotify_Database\Spotify_Database.accdb;'
    )

conn = pyodbc.connect(conn_str)

token = util.prompt_for_user_token(username, scope, 
                                   client_id='408e050241fb4452990a1a129f601f80', 
                                   client_secret='8f0caa3b11e54eed86ece49c4dfe3a3d', 
                                   redirect_uri='http://localhost:8888/callback/')
spotify = spotipy.Spotify(auth=token)
spotify.trace = False

entries = []

cursor = conn.cursor()
cursor.execute("select * from Electronic_Database")

playlists = {'test': 'spotify:playlist:2M1IeXb363IEGYbBnrgZ56'}

# for row in cursor.fetchall():
#     temp = []
#     temp += [row.Artist.split(', ')[0]]
#     song_name = row.Song_Name
#     if row.Extra is not None:
#         song_name += ' ' + row.Extra
#     temp += [song_name]
#     entries += [temp]
# addToPlaylistFromURI(spotify, playlists['test'], getURIs(spotify, entries))

temp = [['Feint', 'We Won\'t be alone']]
addToPlaylistFromURI(spotify, playlists['test'], getURIs(spotify, temp))

timeElapsed = time.time() - start
print('Time elapsed:', '{0:.2f}s'.format(timeElapsed))
# import pyodbc

# conn_str = (
#     r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
#     r'DBQ=C:\Users\thund\Python\Spotify_Database\Spotify_Database.accdb;'
#     )

# conn = pyodbc.connect(conn_str)
# cursor = conn.cursor()
# cursor.execute("select * from Electronic_Database where Genre LIKE '%House%'")
# for row in cursor.fetchall():
#     print(str(row.Artist) + ' - ' + str(row.Song_Name))
#     # genres = row.Genre.split(', ')
#     # print(genres)