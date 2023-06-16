from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from apps.account.models import Profile
from apps.notification.service import SendNotification
from apps.history.service import WorkoutHistoryAction

from .models import Category, Workout, Exercise
from .serializers import (
    CategorySerializers,
    WorkoutListSerializers,
    WorkoutCreateSerializers,
    WorkoutUpdateSerializers,
    WorkoutRetrieveSerializers,
    ExerciseSerializers,
    ExerciseRetrieveSerializers,
    ExerciseUpdateSerializers,
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

    def perform_destroy(self, instance: Workout):
        users_id = list(
            Profile.objects.filter(workout=instance)
            .values_list('owner', flat=True),
        )
        # add event delete workout
        WorkoutHistoryAction().update_workout_users(
            users_id=users_id,
            workout=instance,
            detail_info={
                'datetime': timezone.now().isoformat(),
                'event': (
                    f'Owner {instance.user.username} workout removed workout'
                ),
            },
        )
        # closed history workout
        WorkoutHistoryAction.close_workout_for_users(
            users_id=users_id,
            workout=instance,
        )
        workout_title = instance.title
        instance.exercises.all().delete()
        instance.delete()

        SendNotification().send_notification_at_remove_workout(
            users_id=users_id,
            workout_title=workout_title,
        )


class ExerciseView(viewsets.ModelViewSet):

    queryset = Exercise.objects.select_related('workout').filter(
        publish=True,
        workout__publish=True,
    ).order_by('day')
    serializer_class = ExerciseSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workout', 'day']
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExerciseRetrieveSerializers
        elif (
            self.action == 'update' or
            self.action == 'partial_update'
        ):
            return ExerciseUpdateSerializers
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
