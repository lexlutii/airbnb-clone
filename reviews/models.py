from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):
    """ Review Model Definition """
    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanlines = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f'Review for room "{self.room.name}" by user "{self.user}"'

    class Meta:
        verbose_name = "Review"
        pass
