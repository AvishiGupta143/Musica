from rest_framework import serializers
from .models import Song, Playlist


class SongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('Playlist_Name', 'Songs_In_Playlist', 'Visibility')
        action_fields = {
            'Playlist_Owner': {'fields': ('first_name', 'email')}
        }
        read_only_fields = (['Songs_In_Playlist'])
        depth = 1


class ParticularPlaylistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('Playlist_Name', 'Songs_In_Playlist')
        read_only_fields = (['Songs_In_Playlist'])
        depth = 1


class ParticularSongSerializers(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
