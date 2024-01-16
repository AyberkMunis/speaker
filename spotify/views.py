from re import S
from tkinter.font import ROMAN
from turtle import update
from urllib import response
from django.shortcuts import render, redirect

from .serializers import TasteSerializer
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post, session
from rest_framework import status
from rest_framework.response import Response
from .util import execute_spotify_api_request2, execute_spotify_api_request3, update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens,execute_spotify_api_request
from api.models import Place
import numpy as np
from scipy import spatial
from langid import classify



class AuthURL(APIView):
    def get(self, request, fornat=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-top-read playlist-modify-public playlist-modify-private'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()
    print(response)

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Place.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)

        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""

        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'id': song_id
        }

        self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)
    def update_room_song(self, room, song_id):
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=['current_song'])

class playlisttaste(APIView):
    serilizer_class=TasteSerializer
    def post(self,request,format=None):
        serializer=self.serilizer_class(data=request.data)
        if serializer.is_valid():
            base=serializer.data.get("taste")
            base=base.split("/")
            base=base[4].split("?")
            id=base[0]

            link=f"https://api.spotify.com/v1/playlists/{id}/tracks"
            response=execute_spotify_api_request2(self.request.session.session_key,link=link)
            aft={}
            aft["language"]={}
            aft["tracks"]=[]
            aft["genres"]=set()
            for i in range(len(response["items"])):
                try:
                    artist=response["items"][i]["track"]["artists"][0]["name"]
                except:
                    continue
                sid=response["items"][i]["track"]["id"]
                name=response["items"][i]["track"]["name"]
                aid=response["items"][i]["track"]["artists"][0]["id"]
                link3=f"https://api.spotify.com/v1/artists/{aid}"
                a=execute_spotify_api_request2(self.request.session.session_key,link=link3)
                try:
                    genres=a["genres"]
                    for i in genres:
                        aft["genres"].add(i)
                except:
                    continue
                lang=classify(name)
                if lang[0] in aft["language"]:
                    aft["language"][lang[0]]+=1
                else:
                    aft["language"][lang[0]]=1
                aft["tracks"].append(sid)
                link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                af=execute_spotify_api_request2(self.request.session.session_key,link=link2)
                for k,v in af.items():
                    if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                        if k in aft:
                            aft[k]+=v
                        else:
                            aft[k]=v
                for k,v in aft.items():
                    if k=="language" or k=="tracks" or k=="genres":
                        continue
                    v1=v/len(response["items"])
                    aft[k]=v1
            aft["language"]=sorted(aft["language"].items(), key=lambda x: x[1], reverse=True)

            return Response(aft,status=status.HTTP_200_OK)
        return Response({"msg":"annen"},status=status.HTTP_400_BAD_REQUEST)
class usertaste(APIView):
    def get(self,request,format=None):
        code=self.request.session.get("room_code")
        room=Place.objects.filter(code=code)
        if room.exists() and room[0].host!=self.request.session.session_key:
            room=room[0]
            taste=room.taste
            genre=room.genre
            host=room.host
            base=room.base
            end1="https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10"
            end2="https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=10"
            end3="https://api.spotify.com/v1/me/top/tracks?time_range=medium_term&limit=10"
            t1=execute_spotify_api_request2(self.request.session.session_key,end1)
            t2=execute_spotify_api_request2(self.request.session.session_key,end2)
            t3=execute_spotify_api_request2(self.request.session.session_key,end3)
            tastel=[]
            ids={}
            for k,v in taste.items():
                if k=="language" or k=="tracks" or k=="genres":
                    continue
                tastel.append(v)
            language=str(taste["language"][0][0])
            cos={}
            cos.clear()
            if genre=="none":
                for i in range(len(t1)):
                    artist=t1["items"][i]["artists"][0]["name"]
                    name=t1["items"][i]["name"]
                    sid=t1["items"][i]["id"]
                    lang=classify(name)[0]
                    if (str(lang) != language) or (sid in taste["tracks"]) or self.request.session.get("taste")==code:
                        continue
                    else:
                        link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                        laf=[]
                        af=execute_spotify_api_request2(self.request.session.session_key,link2)
                        for k,v in af.items():
                            if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                laf.append(v)
                        result = 1 - spatial.distance.cosine(tastel, laf)
                        cos[t1["items"][i]["uri"]]=result
                        ids[t1["items"][i]["id"]]=result
                        laf.clear()
                for i in range(len(t2)):
                    artist=t2["items"][i]["artists"][0]["name"]
                    sid=t2["items"][i]["id"]
                    name=t2["items"][i]["name"]
                    lang=classify(name)[0]
                    if (str(lang) != language) or (sid in taste["tracks"]) or self.request.session.get("taste")==code:
                        continue
                    else:
                        sid=t2["items"][i]["id"]
                        link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                        laf=[]
                        af=execute_spotify_api_request2(self.request.session.session_key,link2)
                        for k,v in af.items():
                            if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                laf.append(v)
                        result = 1 - spatial.distance.cosine(tastel, laf)
                        cos[t2["items"][i]["uri"]]=result
                        ids[t2["items"][i]["id"]]=result
                        laf.clear()
                for i in range(len(t3)):
                    artist=t3["items"][i]["artists"][0]["name"]
                    sid=t3["items"][i]["id"]
                    name=t3["items"][i]["name"]
                    lang=classify(name)[0]
                    if (str(lang) != language) or (sid in taste["tracks"]) or self.request.session.get("taste")==code:
                        continue
                    else:
                        link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                        laf=[]
                        af=execute_spotify_api_request2(self.request.session.session_key,link2)
                        for k,v in af.items():
                            if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                laf.append(v)
                        result = 1 - spatial.distance.cosine(tastel, laf)
                        cos[t3["items"][i]["uri"]]=result
                        ids[t3["items"][i]["id"]]=result
                        laf.clear()
            else:
                    for i in range(len(t1)):
                        artist=t1["items"][i]["artists"][0]["name"]
                        name=t1["items"][i]["name"]
                        sid=t1["items"][i]["id"]
                        lang=classify(name)[0]
                        aid=t1["items"][i]["artists"][0]["id"]
                        link3=f"https://api.spotify.com/v1/artists/{aid}"
                        a=execute_spotify_api_request2(self.request.session.session_key,link=link3)

                        genre2=a["genres"]
                        number=0
                        for c in genre2:
                            for b in taste["genres"]:
                                if c==b:
                                    number+=1
                        if (str(lang) != language) or (sid in taste["tracks"]) or number==0 or self.request.session.get("taste")==code:
                            continue
                        else:
                            link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                            laf=[]
                            af=execute_spotify_api_request2(self.request.session.session_key,link2)
                            for k,v in af.items():
                                if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                    laf.append(v)
                            result = 1 - spatial.distance.cosine(tastel, laf)
                            cos[t1["items"][i]["uri"]]=result
                            ids[t1["items"][i]["id"]]=result
                            laf.clear()
                    for i in range(len(t2)):
                        artist=t2["items"][i]["artists"][0]["name"]
                        sid=t2["items"][i]["id"]
                        name=t2["items"][i]["name"]
                        lang=classify(name)[0]
                        aid=t2["items"][i]["artists"][0]["id"]
                        link3=f"https://api.spotify.com/v1/artists/{aid}"
                        a=execute_spotify_api_request2(self.request.session.session_key,link=link3)
                        genre2=a["genres"][0]
                        number=0
                        for c in genre2:
                            for b in taste["genres"]:
                                if c==b:
                                    number+=1
                        if (str(lang) != language) or (sid in taste["tracks"]) or number==0 or self.request.session.get("taste")==code:
                            continue
                        else:
                            sid=t2["items"][i]["id"]
                            link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                            laf=[]
                            af=execute_spotify_api_request2(self.request.session.session_key,link2)
                            for k,v in af.items():
                                if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                    laf.append(v)
                            result = 1 - spatial.distance.cosine(tastel, laf)
                            cos[t2["items"][i]["uri"]]=result
                            ids[t2["items"][i]["id"]]=result
                            laf.clear()
                    for i in range(len(t3)):
                        artist=t3["items"][i]["artists"][0]["name"]
                        sid=t3["items"][i]["id"]
                        name=t3["items"][i]["name"]
                        lang=classify(name)[0]
                        aid=t3["items"][i]["artists"][0]["id"]
                        link3=f"https://api.spotify.com/v1/artists/{aid}"
                        a=execute_spotify_api_request2(self.request.session.session_key,link=link3)
                        genre2=a["genres"][0]
                        number=0
                        for c in genre2:
                            for b in taste["genres"]:
                                if c==b:
                                    number+=1
                        if (str(lang) != language) or (sid in taste["tracks"]) or number==0 or self.request.session.get("taste")==code:
                            continue
                        else:
                            link2=f"https://api.spotify.com/v1/audio-features/{sid}"
                            laf=[]
                            af=execute_spotify_api_request2(self.request.session.session_key,link2)
                            for k,v in af.items():
                                if k=="dancebility" or k=="energy" or k=="loudness" or k=="mode" or k=="speechiness" or k=="acousticness" or k=="liveness" or k=="valence" or k=="tempo":
                                    laf.append(v)
                            result = 1 - spatial.distance.cosine(tastel, laf)
                            cos[t3["items"][i]["uri"]]=result
                            ids[t3["items"][i]["id"]]=result
                            laf.clear()
            cos=sorted(cos.items(), key=lambda x: x[1], reverse=True)
            ids=sorted(ids.items(), key=lambda x: x[1], reverse=True)
            x=0
            y=0
            base=base.split("/")
            base=base[4].split("?")
            idd=base[0]
            tracks=taste["tracks"]
            link3=f"https://api.spotify.com/v1/playlists/{idd}/tracks"
            for i in ids:
                if y==3:
                    break
                tracks.append(i[0])
                y+=1
            room.taste["tracks"]=tracks
            room.save(update_fields=["taste"])



            for i in cos:
                if x==3:
                    break
                js={"uris":[i[0]]}
                d=execute_spotify_api_request3(session_id=host,link=link3,body=js,post_=True)
                print(d)
                js.clear()
                x+=1
            self.request.session["taste"]=code
            return Response(cos,status=status.HTTP_200_OK)



        return Response({"msg":"Bad Request"},status=status.HTTP_400_BAD_REQUEST)
class GetUser(APIView):
    def get(self,request,format=None):
        link="https://api.spotify.com/v1/me"
        a=execute_spotify_api_request2(self.request.session.session_key,link=link)
        if len(a)>0:
            return Response(a,status=status.HTTP_200_OK)
        return Response({"msg":"err"},status=status.HTTP_400_BAD_REQUEST)



