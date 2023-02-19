from django.contrib import admin
from .models import CustomUser, Avatar

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Avatar)

