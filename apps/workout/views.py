from rest_framework import generics, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Workout, Exercise
from .serializers import (
    CategorySerializers,
    WorkoutListSerializers,
    WorkoutCreateSerializers,
    WorkoutUpdateSerializers,
    WorkoutRetrieveSerializers,
    ExerciseSerializers,
    ExerciseRetrieveSerializers,
)
from .permissions import IsEditWorkout, IsEditExercise, IsCreateExercise


class CategoryView(generics.ListAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all().order_by('title')


class WorkoutView(viewsets.ModelViewSet):

    serializer_class = WorkoutListSerializers
    queryset = Workout.objects.select_related(
        'category',
        'user',
    ).filter(publish=True).order_by('created')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'user']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return WorkoutRetrieveSerializers
        if self.action == 'create':
            return WorkoutCreateSerializers
        if self.action == 'update' or self.action == 'partial_update':
            return WorkoutUpdateSerializers
        return super().get_serializer_class()

    def get_permissions(self):
        if (
            self.action == 'update' or
            self.action == 'partial_update' or
            self.action == 'destroy'
        ):
            return [IsEditWorkout()]
        return super().get_permissions()
    # TODO: the method to destroy must also be removed exercise
    # add a deletion history for users who are subscribed to the program


class ExerciseView(viewsets.ModelViewSet):

    queryset = Exercise.objects.select_related('workout').filter(
        publish=True,
        workout__publish=True,
    ).order_by('day')
    serializer_class = ExerciseSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workout', 'day']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExerciseRetrieveSerializers
        return super().get_serializer_class()

    def get_permissions(self):
        if (
            self.action == 'update' or
            self.action == 'partial_update' or
            self.action == 'destroy'
        ):
            return [IsEditExercise()]
        elif self.action == 'create':
            return [IsCreateExercise()]
        return super().get_permissions()
