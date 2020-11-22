from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampedModel):
    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True)

    def __str__(self):
        participants = self.participants.all()
        def get_user_name(u): return u.username
        usernames = map(get_user_name, participants)
        return ", ".join(usernames)

    def count_messages(self):
        return self.messages.count()
    count_messages.short_name = "Number of messages"

    def count_participants(self):
        return self.participants.count()
    count_participants.short_name = "Number of participants"


class Message(core_models.TimeStampedModel):
    content = models.TextField()

    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} says: {self.content}'
