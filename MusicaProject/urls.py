from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.urlpatterns import format_suffix_patterns
from Musica import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('MusicaAPI/Song/', views.SongList.as_view()),
                  path('MusicaAPI/Playlist/', views.PlaylistList.as_view()),
                  path('MusicaAPI/Playlist/<str:id>', views.ParticularPlaylistList.as_view()),
                  path('MusicaAPI/Song/<str:id>', views.ParticularSongList.as_view()),
                  path('Musica/', include('Musica.urls')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
