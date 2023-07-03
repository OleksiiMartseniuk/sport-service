from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    WorkoutHistorySerializer,
    WorkoutHistoryRetrieveSerializer,
)
from .models import WorkoutHistory


class HistoryWorkoutView(viewsets.ReadOnlyModelViewSet):

    queryset = WorkoutHistory.objects.all()
    serializer_class = WorkoutHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkoutHistoryRetrieveSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return WorkoutHistory.objects.filter(
            user=self.request.user,
        ).order_by('id')
