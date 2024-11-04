from django.contrib import admin
from .models import Movie, MovieReport, Rating

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
    
@admin.register(MovieReport)
class MovieReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'reported_by', 'reason', 'status', 'created_at']
    actions = ['approve_report', 'reject_report']

    def approve_report(self, request, queryset):
        for report in queryset:
            report.approve(admin_user=request.user)
        self.message_user(request, "Selected reports have been approved.")

    def reject_report(self, request, queryset):
        for report in queryset:
            report.reject(admin_user=request.user)
        self.message_user(request, "Selected reports have been rejected.")

    approve_report.short_description = "Approve selected reports"
    reject_report.short_description = "Reject selected reports"
