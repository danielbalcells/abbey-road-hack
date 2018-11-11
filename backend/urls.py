from django.urls import register_converter, path

from . import views

urlpatterns = [
    path('search/', views.Search.as_view()),
    path('recommend/<isrc>/', views.Recommend.as_view(), name='recommend')
]
