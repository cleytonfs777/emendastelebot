from django.contrib import admin
from django.urls import include, path

from .views import teleg

urlpatterns = [
    path('', teleg, name='teleg'),

]
