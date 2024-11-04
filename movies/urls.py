from django.urls import path
from .views import ListReportsView, MovieListView, MovieDetailView, MovieCreateView, MovieUpdateView, RatingCreateUpdateView, ReportMovieView, UpdateReportStatusView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/create/', MovieCreateView.as_view(), name='movie-create'),
    path('movies/<int:pk>/update/', MovieUpdateView.as_view(), name='movie-update'),
    path('movies/<int:movie_id>/rate/', RatingCreateUpdateView.as_view(), name='movie-rate'),
    path('movies/<int:movie_id>/report/', ReportMovieView.as_view(), name='report-movie'),
    path('reports/', ListReportsView.as_view(), name='list-reports'),
    path('reports/<int:pk>/status/', UpdateReportStatusView.as_view(), name='update-report-status'),
]
