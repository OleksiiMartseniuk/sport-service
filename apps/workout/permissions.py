from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Workout


class IsEditWorkout(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsEditExercise(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.workout.user == request.user


class IsCreateExercise(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            workout = Workout.objects.filter(
                id=request.data.get('workout'),
                user=request.user,
            )
            return True if workout else False
        return False
