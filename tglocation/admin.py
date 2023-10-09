from django.contrib import admin
from .models import Locations,TgUser
# Register your models here.
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'latitude', 'longitude')

class TgUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'latitude', 'longitude')

admin.site.register(Locations, LocationsAdmin)
admin.site.register(TgUser, TgUserAdmin)