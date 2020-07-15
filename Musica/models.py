from django.db import models
from django.contrib.auth.models import auth, User


class Song(models.Model):
    Name = models.CharField(max_length=9999)
    Album = models.CharField(max_length=9999)
    Artist = models.CharField(max_length=9999)
    Year = models.CharField(max_length=10)
    Song_File = models.FileField()
    Album_Art = models.CharField(max_length=1000000, default='', blank=True)

    def __str__(self):
        return self.Name


class Playlist(models.Model):
    Playlist_Owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Playlist_Name = models.CharField(max_length=999)
    Songs_In_Playlist = models.ManyToManyField(Song, blank=True)
    Visibility = models.CharField(max_length=100)
    Public = models.BooleanField(default=False)

    def __str__(self):
        return self.Playlist_Name + 'by' + self.Playlist_Owner.first_name