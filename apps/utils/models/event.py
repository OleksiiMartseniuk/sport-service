from django.db import models


class Event(models.Model):

    title = models.CharField(
        max_length=255,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f'#{self.id}. {self.title}'
