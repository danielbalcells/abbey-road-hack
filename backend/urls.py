from django.urls import register_converter, path

from . import views

urlpatterns = [
    path('search/', views.Search.as_view())
]
