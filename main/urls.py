from .views import *
from django.urls import path


urlpatterns = [
    path('', main_page, name='home')
]
