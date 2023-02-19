from django.shortcuts import render
from rest_framework.views import APIView
import random
# from twilio.rest import Client
from django.http import JsonResponse
# Create your views here.


class SendOtp(APIView):
    def post(self, request):
        account_sid = 'ACb45bfbaed5f034c3200150021430f255'
        auth_token = '53b7069e19cd73cdf73bef2487aff889'
        number = request.data['number']
        client = Client(account_sid, auth_token)
        otp = generateOTP()
        body = 'Your OTP is '+ str(otp)
        message = client.messages.create(from_='', body=body, to=number)
        if message.sid:
            print('Sent successful')
            return JsonResponse({'success': True})
        else:
            print('Failed')
            return JsonResponse({'success': False})



def generateOTP():

    return random.randrange(100000, 999999)
