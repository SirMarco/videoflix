from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True)  # Gibt die Namen der Kategorien zurück
    
    class Meta:
        model = Video
        fields = '__all__'