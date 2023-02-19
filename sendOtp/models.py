import os
# from twilio.rest import Client
from django.db import models

# Create your models here.


class Score(models.Model):
    result = models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

    def save(self, *args, **kwargs):
        if self.result < 70:
            account_sid = os.environ['TWILIO_ACCOUNT_SID']
            auth_token = os.environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f'Hi,the current result is bad - {self.result}',
                from_='+13344328644',
                to='+996777183818'
            )

            print(message.sid)
        return super().save(*args, **kwargs)
