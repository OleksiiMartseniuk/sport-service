def exercise_image_path(instance, filename: str) -> str:
    return f"workouts/{instance.workout.id}/{filename}"
