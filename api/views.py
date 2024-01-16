from os import stat
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from requests import request
from rest_framework import generics,status
from .serializers import PlaceSerializer,CreatePlaceSerializer, UpdatePlaceSerializer
from .models import Place
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
# Create your views here.
class PlaceView(generics.ListAPIView):
    queryset=Place.objects.all()
    serializer_class=PlaceSerializer
class GetRoom(APIView):
    serializer_class=PlaceSerializer
    lookup_url_kwarg='code'
    def get(self,request,format=None):
        code =request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room=Place.objects.filter(code=code)
            if len(room)>0:
                data=PlaceSerializer(room[0]).data
                data['is_host']=self.request.session.session_key == room[0].host
                return Response(data,status=status.HTTP_200_OK)
            return Response({"Room Not Found":"Invalid Room Code"},status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request":"Code parameter does not work"},status=status.HTTP_400_BAD_REQUEST)
class JoinRoom(APIView):
    lookup_url_kwarg='code'
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code=request.data.get(self.lookup_url_kwarg)
        if code != None:
            roomr=Place.objects.filter(code=code)
            if len(roomr)>0:
                room=roomr[0]
                self.request.session["room_code"]=code
                return Response({"message":"room joined"},status=status.HTTP_200_OK)
            return Response({"message":"room joined"},status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request':'Invalid post data'},status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    serializer_class=CreatePlaceSerializer
    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            genre=serializer.data.get('genre')
            taste=serializer.data.get('taste')
            base=serializer.data.get('base')
            name=serializer.data.get('name')

            host=self.request.session.session_key
            queryset=Place.objects.filter(host=host)
            if queryset.exists():
                room=queryset[0]
                room.genre=genre
                room.taste=taste
                room.base=base
                room.name=name
                room.save(update_fields=['genre','taste','base','name'])
                self.request.session["room_code"]=room.code
                return Response(PlaceSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room=Place(host=host,genre=genre,taste=taste,base=base,name=name)
                room.save()
                self.request.session["room_code"]=room.code
                return Response(PlaceSerializer(room).data,status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
class UserInRoom(APIView):
    def get(self,request,format=None):
        data={
            'code':self.request.session.get('room_code')
        }
        return JsonResponse(data,status=status.HTTP_200_OK)
class LeaveRoom(APIView):
    def post(self,request,format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id=self.request.session.session_key
            room_results=Place.objects.filter(host=host_id)
            if len(room_results)>0:
                room=room_results[0]
                room.delete()
        return Response({"Message":"Success"},status=status.HTTP_200_OK)
class UpdateRoom(APIView):
    serializer_class=UpdatePlaceSerializer
    def patch(self,request,format=None):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            genre=serializer.data.get("genre")
            code=serializer.data.get("code")
            queryset=Place.objects.filter(code=code)
            if not queryset.exists():
                return Response({"msg":"Room not found"},status=status.HTTP_404_NOT_FOUND)
            room=queryset[0]
            user_id=self.request.session.session_key
            if room.host!=user_id:
                return Response({"msg":"You are not allowed to change"},status=status.HTTP_403_FORBIDDEN)
            room.genre=genre
            room.save(update_fields=['genre'])
            return Response(PlaceSerializer(room).data,status=status.HTTP_201_CREATED)
            
        return Response({"Bad Request":"Invalid Data"},status=status.HTTP_400_BAD_REQUEST)




