from getpass import getuser
from django.urls import path
from .views import AuthURL, CurrentSong, playlisttaste, spotify_callback, IsAuthenticated, usertaste,GetUser

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path("taste",playlisttaste.as_view()),
    path("getu-taste",usertaste.as_view()),
    path("get-current",CurrentSong.as_view()),
    path("get-user",GetUser.as_view())
]
