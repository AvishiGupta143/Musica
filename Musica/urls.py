from django.urls import path
from Musica import views

urlpatterns = [
    path('', views.Homepage.as_view(), name='Homepage'),
    path('Register', views.Register, name='Register'),
    path('Login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('CheckEmail', views.CheckEmail, name='CheckEmail'),
    path('AddSongs', views.AddSongs.as_view(), name='AddSongs'),
    path('CreatePlaylist', views.CreatePlaylist.as_view(), name='CreatePlaylist'),
    path('Playlists', views.Playlists.as_view(), name='Playlists'),
    path('Songs', views.Songs.as_view(), name='Songs'),
    path('Automate', views.Automate, name='Automate'),
    path('Users', views.Users.as_view(), name='Users'),
    path('Profile/<str:name>', views.Profile.as_view(), name='Profile'),
    path('SinglePlaylist/<str:id>', views.SinglePlaylist.as_view(), name='SinglePlaylist'),
    path('UserPlaylist/<str:id>', views.UserPlaylist.as_view(), name='UserPlaylist'),
    path('RemoveSongFromPlaylist', views.RemoveSongFromPlaylist, name='RemoveSongFromPlaylist'),
    path('AddToPlaylist', views.AddToPlaylist, name='AddToPlaylist'),
    path('CheckLoginPassword', views.CheckLoginPassword, name='CheckLoginPassword'),
    path('GiveDetails', views.GiveDetails, name='GiveDetails'),
    path('DeletePlaylist', views.DeletePlaylist, name='DeletePlaylist'),
    path('MakePrivate', views.MakePrivate, name='MakePrivate'),
    path('CopyTo', views.CopyTo, name='CopyTo'),
]
