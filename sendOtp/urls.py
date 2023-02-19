from django.urls import path

from .views import SendOtp

urlpatterns = [
    path('send_otp/', SendOtp.as_view())
]
