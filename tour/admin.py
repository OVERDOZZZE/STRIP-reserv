from django.contrib import admin
from .models import *
# Register your models here.


class TourAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tour, TourAdmin)
admin.site.register(Review)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Place)



