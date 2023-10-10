from django.contrib import admin
from .models import Tours, ToursMembers, CategoryTours, ReviewsTours, LikesTours, LikesReviews


class ToursAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date',
                    'time_start', 'price', 'max_members')
    list_filter = ('organizer', 'category', 'date')
    search_fields = ('title', 'description', 'geolocation_name', 'route')
    filter_horizontal = ('category',)


class ToursMembersAdmin(admin.ModelAdmin):
    list_display = ('user', 'tours')
    list_filter = ('tours', 'user')


class CategoryToursAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ReviewsToursAdmin(admin.ModelAdmin):
    list_display = ('user', 'tours', 'title', 'created_at')
    list_filter = ('tours', 'user')


class LikesToursAdmin(admin.ModelAdmin):
    list_display = ('user', 'tours', 'created_at')
    list_filter = ('tours', 'user')


class LikesReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')


admin.site.register(Tours, ToursAdmin)
admin.site.register(ToursMembers, ToursMembersAdmin)
admin.site.register(CategoryTours, CategoryToursAdmin)
admin.site.register(ReviewsTours, ReviewsToursAdmin)
admin.site.register(LikesTours, LikesToursAdmin)
admin.site.register(LikesReviews, LikesReviewsAdmin)
