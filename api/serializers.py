from rest_framework import serializers
from .models import Place
class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields=('id','code','host','taste','created_at','genre','base','name')
class CreatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Place
        fields=('id','genre','taste','base','name')
class UpdatePlaceSerializer(serializers.ModelSerializer):
    code=serializers.CharField(validators=[])
    class Meta:
        model=Place
        fields=('genre','code')
