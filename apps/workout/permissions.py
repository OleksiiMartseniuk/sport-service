from rest_framework.permissions import IsAuthenticated


class IsEditWorkout(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
