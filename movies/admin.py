from django.contrib import admin
from .models import Movie, Rating

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'released_at', 'duration', 'created_by', 'avg_rating', 'total_ratings']
    search_fields = ['title', 'genre']
    list_filter = ['genre', 'released_at']
    readonly_fields = ['avg_rating', 'total_ratings']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'score', 'created_at']
    list_filter = ['score']
    search_fields = ['movie__title', 'user__username']
