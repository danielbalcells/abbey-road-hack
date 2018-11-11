import csv
import sys
from dateutil.parser import parse

from backend import models

def ingest(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        for line in reader:
            track = models.Track(
                isrc=line.get('isrc', ''),
                spotify_track_uri=line.get('spotify_track_uri', ''),
                title=line.get('title', 'Unknown title'),
                artist=line.get('artist_name', 'Unknown artist'),
                tempo=float(line.get('tempo', -1) or -1),
                instrumentalness=float(line['instrumentalness'] or 0),
                energy=float(line.get('energy', 0) or 0),
                year=parse(line['release_date'] or '1970').year,
                cover_art_url=line['coverart']
            )
            track.save()

