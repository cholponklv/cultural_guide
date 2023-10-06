from django.contrib import admin
from .models import Meeting, MeetingMembers



class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date_time', 'max_members', 'price')
    list_filter = ('organizer',)
    search_fields = ('title', 'description', 'geolocation_name')


class MeetingMembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'meeting')
    list_filter = ('meeting', 'user')

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingMembers, MeetingMembersAdmin)
