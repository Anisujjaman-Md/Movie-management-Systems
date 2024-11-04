from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    released_at = models.DateField()
    duration = models.PositiveIntegerField()
    genre = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    avg_rating = models.FloatField(default=0, editable=False)
    total_ratings = models.PositiveIntegerField(default=0, editable=False)
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_avg_rating(self):
        ratings = Rating.objects.filter(movie=self)
        self.avg_rating = ratings.aggregate(Avg('score'))['score__avg'] or 0
        self.total_ratings = ratings.count()
        self.save(update_fields=['avg_rating', 'total_ratings'])

    def __str__(self):
        return self.title

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('movie', 'user')  # One rating per user per movie

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_avg_rating()

class MovieReport(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reports")
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_submitted")
    reason = models.CharField(max_length=255)
    details = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        default="pending"
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_reviewed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def approve(self, admin_user):
        self.status = "approved"
        self.reviewed_by = admin_user
        self.save()

    def reject(self, admin_user):
        self.status = "rejected"
        self.reviewed_by = admin_user
        self.save()