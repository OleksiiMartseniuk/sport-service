import uuid


def exercise_image_path(instance, filename: str) -> str:
    exe = filename.split('.')[-1]
    return f"workouts/{instance.workout.id}/exercises/{uuid.uuid4()}.{exe}"
