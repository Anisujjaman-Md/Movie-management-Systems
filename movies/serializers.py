from rest_framework import serializers
from .models import Movie, Rating, MovieReport

class MovieSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    avg_rating = serializers.FloatField(read_only=True)
    total_ratings = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'released_at', 'duration', 'genre', 'created_by', 
                  'avg_rating', 'total_ratings', 'language', 'created_at', 'updated_at']

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Rating
        fields = ['id', 'movie', 'user', 'score', 'created_at', 'updated_at']


class MovieReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReport
        fields = ['id', 'movie', 'reason', 'details', 'status', 'reported_by', 'created_at']
        read_only_fields = ['status', 'reported_by', 'created_at']

class MovieReportAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReport
        fields = ['id', 'status']