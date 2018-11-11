from rest_framework import serializers
from . import models

class TracksSerializer(serializers.ModelSerializer):
    recommendations = serializers.HyperlinkedIdentityField(
        read_only=True, view_name='recommend', lookup_field='isrc'
    )
    
    class Meta:
        model = models.Track
        fields = '__all__'
