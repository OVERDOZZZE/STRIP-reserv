from django.urls import path, include
from .views import *


urlpatterns = [
    path('user_profile/', user_profile, name='user_profile'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('activate/<uid64>/<token>', activate, name='activate'),
    path('api_registration/', register),
    path('api_authorization/', authorization)
]

