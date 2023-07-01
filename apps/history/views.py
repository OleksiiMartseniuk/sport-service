from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import WorkoutHistorySerializer
from .models import WorkoutHistory


class HistoryWorkoutView(viewsets.ReadOnlyModelViewSet):

    serializer_class = WorkoutHistorySerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkoutHistory.objects.all()
