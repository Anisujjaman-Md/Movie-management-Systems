from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Movie, MovieReport, Rating
from .serializers import MovieReportSerializer, MovieSerializer, RatingSerializer, MovieReportSerializer, MovieReportAdminSerializer
from rest_framework.exceptions import PermissionDenied

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

class MovieCreateView(generics.CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class MovieUpdateView(generics.UpdateAPIView):
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Movie.objects.filter(created_by=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.updated_at = instance.updated_at  # Ensure `updated_at` doesn’t change on `avg_rating` updates

class RatingCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        rating, _ = Rating.objects.get_or_create(movie=self.get_movie(), user=self.request.user)
        return rating

    def get_movie(self):
        movie_id = self.kwargs.get('movie_id')
        return generics.get_object_or_404(Movie, id=movie_id)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only modify your own ratings.")
        serializer.save()


class ReportMovieView(generics.CreateAPIView):
    serializer_class = MovieReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        movie_id = self.kwargs['movie_id']
        movie = generics.get_object_or_404(Movie, id=movie_id)
        serializer.save(reported_by=self.request.user, movie=movie)


class ListReportsView(generics.ListAPIView):
    queryset = MovieReport.objects.all()
    serializer_class = MovieReportSerializer
    permission_classes = [permissions.IsAdminUser]


class UpdateReportStatusView(generics.UpdateAPIView):
    queryset = MovieReport.objects.all()
    serializer_class = MovieReportAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, *args, **kwargs):
        report = self.get_object()
        status_choice = request.data.get('status')

        if status_choice not in ['approved', 'rejected']:
            return Response({'error': 'Invalid status choice.'}, status=status.HTTP_400_BAD_REQUEST)

        if status_choice == 'approved':
            report.approve(admin_user=request.user)
        elif status_choice == 'rejected':
            report.reject(admin_user=request.user)

        return Response({'message': f'Report {status_choice} successfully.'})

    queryset = MovieReport.objects.all()
    serializer_class = MovieReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id):
        movie = generics.get_object_or_404(Movie, id=movie_id)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(reported_by=request.user, movie=movie)
            return Response({"message": "Movie report submitted successfully.", "report": serializer.data}, status=status.HTTP_201_CREATED)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)