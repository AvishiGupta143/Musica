from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.views.generic import View, TemplateView
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import check_password
import json
import random
from .models import Song, Playlist
import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Song, Playlist
from .serializers import SongSerializers, PlaylistSerializers, ParticularPlaylistSerializers, ParticularSongSerializers


class SongList(APIView):

    def get(self, request):
        AllSongs = Song.objects.all()
        serializer = SongSerializers(AllSongs, many=True)
        return Response(serializer.data)


class PlaylistList(APIView):

    def get(self, request, *args, **kwargs):
        AllPlaylist = Playlist.objects.all()
        serializer = PlaylistSerializers(AllPlaylist, many=True)
        return Response(serializer.data)


class ParticularPlaylistList(APIView):

    def get(self, request, *args, **kwargs):
        AllPlaylist = Playlist.objects.get(id=self.kwargs['id'])
        serializer = ParticularPlaylistSerializers(AllPlaylist)
        return Response(serializer.data)


class ParticularSongList(APIView):

    def get(self, request, *args, **kwargs):
        print(self.kwargs)
        SONG = Song.objects.get(id=self.kwargs['id'])
        serializer = ParticularSongSerializers(SONG)
        return Response(serializer.data)


class Homepage(TemplateView):
    template_name = 'Home.html'


class AddSongs(View):
    template_name = 'AddSongs.html'
    initial = {}

    def get(self, request, *args, **kwargs):
        Data = self.initial
        return render(self.request, self.template_name, Data)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            New = Song()
            New.Name = request.POST['SongName']
            New.Album = request.POST['Album']
            New.Artist = request.POST['Artist']
            New.Year = request.POST['Year']
            try:
                base_url = f"https://www.saavn.com/api.php?__call=autocomplete.get&_marker=0&query={request.POST['SongName']}&ctx=android&_format=json&_marker=0"
                response = requests.get(base_url)
                New.Album_Art = response.json()['albums']['data'][0]['image']
            except Exception as e:
                print(e)
            if 'File' in request.POST:
                New.Song_File = request.POST['File']
            else:
                New.Song_File = request.FILES['File']
            New.save()
            return HttpResponseRedirect('/Musica')


class CreatePlaylist(View):
    initial = {'Songs': Song.objects.all()}
    template_name = 'CreatePlaylist.html'

    def get(self, request, *args, **kwargs):
        Data = self.initial
        return render(request, self.template_name, Data)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print(request.POST)
            New = Playlist()
            New.Playlist_Name = request.POST['Name']
            New.Playlist_Owner = request.user
            New.Visibility = 'Public'
            New.save()
            for i in request.POST.keys():
                if i != 'csrfmiddlewaretoken' and i != 'Name':
                    New.Songs_In_Playlist.add(Song.objects.get(id=i))
                    New.save()
            return HttpResponseRedirect('/Musica/Playlists')


class Playlists(TemplateView):
    template_name = 'Playlists.html'

    def get_context_data(self, **kwargs):
        # print(self.kwargs['id'])
        Data = super().get_context_data(**kwargs)
        Data['Playlists'] = Playlist.objects.filter(Playlist_Owner=self.request.user)
        return Data


class UserPlaylist(TemplateView):
    template_name = 'UserPlaylist.html'

    def get_context_data(self, **kwargs):
        # print(self.kwargs['id'])
        d = []
        Data = super().get_context_data(**kwargs)
        Data['Playlist'] = Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.order_by('Name')
        Data.update({'Playlist_ID': self.kwargs['id']})
        Data.update({'PlaylistName': Playlist.objects.get(id=self.kwargs['id']).Playlist_Name})
        Data.update({'Visibility': Playlist.objects.get(id=self.kwargs['id']).Visibility})
        Data.update({'Playlists': Playlist.objects.exclude(id=self.kwargs['id'])})
        for i in Song.objects.order_by('Name'):
            if i not in Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.all():
                d.append(i)
        Data.update({'Songs': d})
        return Data


def RemoveSongFromPlaylist(request):
    id = request.POST['Playlist']
    idS = request.POST['Song']
    Playlist.objects.get(id=id).Songs_In_Playlist.remove(Song.objects.get(id=idS))
    ctx = {
        'key': 'done',
    }
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def AddToPlaylist(request):
    ToAdd = request.POST.getlist('Songs[]')
    id = request.POST['Playlist_ID']
    for idS in ToAdd:
        Playlist.objects.get(id=id).Songs_In_Playlist.add(Song.objects.get(id=idS))
    ctx = {
        'key': 'done',
    }
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def GiveDetails(request):
    New = Song.objects.get(id=request.POST['Song'])
    ctx = {
        'Name': New.Name,
        'Album': New.Album,
        'Artist': New.Artist,
        'Year': New.Year,
        'Album_Art': New.Album_Art,
    }
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def DeletePlaylist(request):
    id = request.POST['DeletePlaylist']
    Playlist.objects.get(id=id).delete()
    return redirect('/Musica/Playlists')


class SinglePlaylist(TemplateView):
    template_name = 'SinglePlaylist.html'

    def get_context_data(self, **kwargs):
        # print(self.kwargs['id'])
        Data = super().get_context_data(**kwargs)
        Data['Songs_by_Name'] = Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.order_by('Name', 'Artist',
                                                                                                      'Album')
        Data.update({'Songs_by_Album': Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.order_by('Album',
                                                                                                             'Name',
                                                                                                             'Artist')})
        Data.update({'Songs_by_Artist': Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.order_by('Artist',
                                                                                                              'Name',
                                                                                                              'Album')})
        Data.update({'Songs_by_Year': Playlist.objects.get(id=self.kwargs['id']).Songs_In_Playlist.order_by('Year',
                                                                                                            'Name',
                                                                                                            'Album',
                                                                                                            'Artist')})
        Data.update({'Playlist_Name': Playlist.objects.get(id=self.kwargs['id']).Playlist_Name})
        Data.update({'Visibility': Playlist.objects.get(id=self.kwargs['id']).Visibility})
        Data.update({'Owner': Playlist.objects.get(id=self.kwargs['id']).Playlist_Owner.username})
        return Data


class Profile(TemplateView):
    template_name = 'Profile.html'

    def get_context_data(self, **kwargs):
        print(self.kwargs['name'])
        Data = super().get_context_data(**kwargs)
        Data['i'] = User.objects.get(username=self.kwargs['name'])
        return Data


class Users(TemplateView):
    template_name = 'Users.html'

    def get_context_data(self, **kwargs):
        # print(self.kwargs['id'])
        Data = super().get_context_data(**kwargs)
        Data['UserData'] = User.objects.all()
        Data.update({'Playlist': Playlist.objects.all()})
        return Data


class Songs(TemplateView):
    template_name = 'Songs.html'

    def get_context_data(self, **kwargs):
        Data = super().get_context_data(**kwargs)
        Data['Songs'] = Song.objects.order_by('Name')
        return Data


def Register(request):
    print(request.POST)
    A = 'Musica_' + str(random.randint(0, 99999)) + '_' + request.POST['Name'].split()[0]
    while True:
        if User.objects.filter(username=A).exists():
            pass
        else:
            break
    New = User()
    a = request.POST['Name']
    a = a.split()
    if len(a) > 1:
        New.first_name = a[0]
        New.last_name = a[len(a) - 1]
    else:
        New.first_name = a[0]
    New.username = A
    New.email = request.POST['Email']
    New.set_password(request.POST['Password1'])
    New.save()
    ctx = {
        'key': 'done', 'Usernamegenertaed': A,
    }
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def Login(request):
    print(request.POST)
    user = auth.authenticate(username=User.objects.get(email=request.POST['Email']).username,
                             password=request.POST['Password'])
    auth.login(request, user)
    return redirect('/Musica')


def Logout(request):
    auth.logout(request)
    return redirect('/Musica')


def CheckEmail(request):
    message = ""
    if User.objects.filter(email=request.POST['Email']).exists():
        message = 'Exists'
    else:
        message = 'Not'
    ctx = {'Result': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def Automate(request):
    for i in Song.objects.all():
        if i.Album_Art == '':
            try:
                base_url = f"https://www.saavn.com/api.php?__call=autocomplete.get&_marker=0&query={i.Name}&ctx=android&_format=json&_marker=0"
                response = requests.get(base_url)
                New = Song.objects.get(Name=i.Name)
                New.Album_Art = response.json()['albums']['data'][0]['image']
                New.save()
            except Exception as e:
                print(e)
    return redirect('/Musica')


def MakePrivate(request):
    if request.method == 'POST':
        New = Playlist.objects.get(id=request.POST['id'])
        if New.Visibility == 'Public':
            New.Visibility = 'Private'
        else:
            New.Visibility = 'Public'
        New.save()
        ctx = {'Result': New.Visibility}
        return HttpResponse(json.dumps(ctx), content_type='application/json')


def CopyTo(request):
    message = ""
    S_ID = request.POST['S_ID']
    P_ID = request.POST['P_ID']
    if Playlist.objects.get(id=P_ID).Songs_In_Playlist.filter(id=S_ID).exists():
        message = 'Already In Playlist'
    else:
        message = 'Added'
        Playlist.objects.get(id=P_ID).Songs_In_Playlist.add(Song.objects.get(id=S_ID))
    ctx = {'Result': message, 'AddedTo': Playlist.objects.get(id=P_ID).Playlist_Name}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


def CheckLoginPassword(request):
    message = ""
    if check_password(request.POST['Password'], User.objects.get(email=request.POST['Email']).password):
        message = 'Done'
    else:
        message = 'No'
    ctx = {'Result': message}

    return HttpResponse(json.dumps(ctx), content_type='application/json')
