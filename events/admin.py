from django.contrib import admin
from .models import Events, CategoryEvents, CommentsEvents, LikesEvents, LikesComments

class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time_start', 'time_end', 'organizer')
    list_filter = ('category', 'priority', 'organizer')
    search_fields = ('title', 'description', 'geolocation_name')
   
class CategoryEventsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class CommentsEventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('events',)
    search_fields = ('title', 'user__username')

class LikesEventsAdmin(admin.ModelAdmin):
    list_display = ('user', 'events', 'created_at')
    list_filter = ('events', 'user')
    search_fields = ('user__username',)

class LikesCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'comments', 'created_at')
    list_filter = ('comments', 'user')
    search_fields = ('user__username',)

admin.site.register(Events, EventsAdmin)
admin.site.register(CategoryEvents, CategoryEventsAdmin)
admin.site.register(CommentsEvents, CommentsEventsAdmin)
admin.site.register(LikesEvents, LikesEventsAdmin)
admin.site.register(LikesComments, LikesCommentsAdmin)
