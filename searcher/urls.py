from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('profile/', views.view_profile, name='profile'),
    path('csvtodata/', views.csvtodata, name='csvtodata'),
]