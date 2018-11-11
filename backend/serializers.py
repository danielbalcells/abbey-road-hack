from rest_framework import serializers
from . import models

class TracksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Track
        fields = '__all__'
