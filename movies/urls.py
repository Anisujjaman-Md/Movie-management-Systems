from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, RatingCreateUpdateView, MovieReportView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie-create'),
    path('movies/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movies/<int:movie_id>/rate/', RatingCreateUpdateView.as_view(), name='movie-rate'),
    path('movies/report/', MovieReportView.as_view(), name='movie-report'),
]
