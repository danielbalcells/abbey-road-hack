import csv
import copy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dateutil.parser import parse

ccm = SpotifyClientCredentials(
    client_secret='898f5cbf04244d7d88392cb3f63a37c7',
    client_id='72d7c8ce22bb4e5f876c1c008829c6bd'
)

spotify = spotipy.Spotify(client_credentials_manager=ccm)

def group(iterator, count):
    itr = iter(iterator)
    while True:
        yield list([itr.__next__() for i in range(count)])

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def add_popularity(tracks):
    tracks_w_popularity = copy.copy(tracks)
    track_ids = []
    for x in tracks_w_popularity:
        if 'spotify' in x['spotify_track_uri']:
            track_ids.append(x['spotify_track_uri'])
        else:
            track_ids.append('0')
    print('getting popularity')
    stracks = spotify.tracks(tracks=track_ids)['tracks']
    for i, t in enumerate(stracks):
        if t:
            tracks_w_popularity[i]['popularity'] = t['popularity']
        else:
            tracks_w_popularity[i]['popularity'] = None
    return tracks_w_popularity


def get_features(tracks):
    track_ids = []
    for x in tracks:
        if 'spotify' in x['spotify_track_uri']:
            track_ids.append(x['spotify_track_uri'])
        else:
            track_ids.append('0')
    print('getting features')
    sfeatures = spotify.audio_features(tracks=track_ids)
    keys = ['energy', 'instrumentalness', 'tempo']
    features = []
    for i, t in enumerate(sfeatures):
        featdict = {}
        if t:
            for k in keys:
                featdict[k] = t[k]
        else:
            for k in keys:
                featdict[k] = None
        features.append(featdict)
    return features

def add_track_info(tracks):
    tracks_w_info = copy.copy(tracks)
    track_ids = []
    for x in tracks_w_info:
        if 'spotify' in x['spotify_track_uri']:
            track_ids.append(x['spotify_track_uri'])
        else:
            track_ids.append('0')
    print('getting info')
    stracks = spotify.tracks(tracks=track_ids)['tracks']
    for i, t in enumerate(stracks):
        if t:
            tracks_w_info[i]['title'] = t['name']
            tracks_w_info[i]['artist'] = ', '.join([a['name'] for a in t['artists']])
            tracks_w_info[i]['album_id'] = t['album']['id']
        else:
            tracks_w_info[i]['title'] = None
            tracks_w_info[i]['artist'] = None
            tracks_w_info[i]['album_id'] = None
    return tracks_w_info

def get_album_info(tracks):
    album_ids = []
    stracks = spotify.tracks(tracks=[t['spotify_track_uri'] for t in tracks])
    for x in stracks['tracks']:
        if x['album']['id']:
            album_ids.append(x['album']['id'])
        else:
            album_ids.append('0')
    coverarts = []
    for g in chunks(album_ids, 15):
        print('getting albums')
        salbums = spotify.albums(albums=g)['albums']
        for i, a in enumerate(salbums):
            if a:
                try:
                    coverart = sorted(
                        a['images'], key=lambda x: x['width'], reverse=True
                    )[0]['url']
                except:
                    coverart = None
            else:
                coverart = None
            coverarts.append(coverart)
    return coverarts

def get_extra_infos(tracks):
    features = get_features(tracks)
    album_infos = get_album_info(tracks)
    extra_info = [
        {**feat, **{'coverart': album_infos[i]}} for i, feat in enumerate(features)
    ]
    return extra_info

if __name__ == '__main__':
    with open('/Users/ecalabuig/Downloads/db_import.csv', 'w') as fout:
        with open('/Users/ecalabuig/Downloads/prepared.csv') as fin:
            r = csv.DictReader(fin)
            extra_fieldnames = [
                'instrumentalness', 'tempo', 'energy', 'coverart'
            ]
            w = csv.DictWriter(fout, fieldnames=r.fieldnames+extra_fieldnames)
            w.writeheader()
            tracks = []
            #import pudb; pudb.set_trace()
            for i, row in enumerate(r):
                tracks.append(row)
                if (i+1) % 50 == 0:
                    extra_infos = get_extra_infos(tracks)
                    to_write = []
                    for i, t in enumerate(tracks):
                        to_write.append({**t, **extra_infos[i]})
                    w.writerows(to_write)
                    tracks = []

#if __name__ == '__main__':
#    with open('/Users/ecalabuig/Downloads/popularity.csv', 'w') as fout:
#        with open('/Users/ecalabuig/Downloads/FullFilewithHeader.csv') as fin:
#            r = csv.DictReader(fin)
#            new_fieldnames = copy.copy(r.fieldnames)
#            new_fieldnames.append('popularity')
#            w = csv.DictWriter(fout, fieldnames=new_fieldnames)
#            w.writeheader()
#            tracks = []
#            for i, row in enumerate(r):
#                tracks.append(row)
#                if (i+1) % 50 == 0:
#                    tracks_w_popularity = add_popularity(tracks)
#                    w.writerows(tracks_w_popularity)
#                    tracks = []
