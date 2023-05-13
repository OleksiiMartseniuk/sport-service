from rest_framework import generics, viewsets

from .models import Category, Workout
from .serializers import (
    CategorySerializers,
    WorkoutListSerializers,
    WorkoutCreateSerializers,
    WorkoutUpdateSerializers,
    WorkoutRetrieveSerializers,
)
from .permissions import IsEditWorkout


class CategoryView(generics.ListAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all().order_by('title')


class WorkoutView(viewsets.ModelViewSet):

    serializer_class = WorkoutListSerializers
    queryset = Workout.objects.filter(publish=True).order_by('created')
    permission_classes = [IsEditWorkout]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkoutRetrieveSerializers
        if self.action == 'create':
            return WorkoutCreateSerializers
        if self.action == 'update' or self.action == 'partial_update':
            return WorkoutUpdateSerializers
        return super().get_serializer_class()
