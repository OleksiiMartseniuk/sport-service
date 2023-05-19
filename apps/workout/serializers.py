from rest_framework import serializers

from apps.account.serializers import UserCustomSerializer

from .models import Category, Workout, Exercise


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class WorkoutSerializers(serializers.ModelSerializer):

    class Meta:
        model = Workout
        exclude = ['publish']


class WorkoutListSerializers(WorkoutSerializers):

    user = serializers.PrimaryKeyRelatedField(read_only=True)


class WorkoutCreateSerializers(WorkoutSerializers):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )


class WorkoutUpdateSerializers(WorkoutSerializers):

    class Meta:
        model = Workout
        fields = ['title']


class WorkoutRetrieveSerializers(WorkoutSerializers):

    category = CategorySerializers()
    user = UserCustomSerializer()


class ExerciseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        exclude = ['publish']


class ExerciseRetrieveSerializers(ExerciseSerializers):

    workout = WorkoutRetrieveSerializers()
