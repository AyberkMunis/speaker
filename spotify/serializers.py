from rest_framework import serializers
from .models import Taste
class TasteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Taste
        fields=('id','taste')