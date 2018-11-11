from operator import and_
from django.shortcuts import render
from rest_framework import generics
from django.db.models import Q
from functools import reduce
from django.contrib.postgres.search import SearchVector

from . import models, serializers

import similarity_engine

class Filterable:

    filter_dict = {}

    def build_filter(self, params):
        filters = []
        for p in params.keys():
            if p in self.filter_dict:
                filters.append((self.filter_dict[p], params[p]))

        if filters:
            q_list = [Q(f) for f in filters]
        else:
            q_list = [Q()]
        return reduce(and_, q_list)


class Search(generics.ListAPIView):
    
    serializer_class = serializers.TracksSerializer

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        qs = models.Track.objects.all()
        if q is not None:
            qs = qs.annotate(search=SearchVector('title', 'artist'))
        qs = qs.filter(search=q)
        return qs


class Recommend(generics.ListAPIView):

    serializer_class = serializers.TracksSerializer

    def get_queryset(self):
        isrc = self.kwargs.get('isrc', None)
        recommended_isrcs = similarity_engine.recommend(isrc)
        recommended_isrcs.remove(isrc)
        qs = models.Track.objects.filter(isrc__in=recommended_isrcs)
        return qs
