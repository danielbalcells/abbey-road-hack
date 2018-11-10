from django.db import models

# Create your models here.

class Track(models.Model):

    isrc =  models.CharField(max_length=200)
    spotify_track_uri = models.CharField(max_length=200)
    cover_art_url = models.TextField()
    title = models.TextField()
    artist = models.TextField()
    tempo = models.FloatField()
    instrumentalness = models.FloatField()
    energy = models.FloatField()
    year = models.IntegerField()


class TrackGenres(models.Model):

    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Genre(models.Model):

    name = models.CharField(max_length=500)
