import csv
import sys

from backend import models

def ingest(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        for line in reader:
            try:
                track = models.Track(
                    isrc=line.get('isrc', ''),
                    spotify_track_uri=line.get('spotify_uri', ''),
                    title=line.get('title', 'Unknown title'),
                    artist=line.get('artist_name', 'Unknown artist'),
                    tempo=float(line.get('spotify_tempo', -1) or -1),
                    instrumentalness=float(line.get('spotify_instrumentalness',
                                                    0) or 0),
                    energy=float(line.get('spotify_energy', 0) or 0),
                    year=line.get('release_date', '1970')[:4])
                track.save()
