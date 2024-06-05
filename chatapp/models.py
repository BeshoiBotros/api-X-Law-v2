from django.db import models
from users import models as users_models

class ChatRoom(models.Model):
    name  = models.CharField(max_length=255, null=False, blank=False, unique=True)
    users = models.ManyToManyField(users_models.CustomUser)

    def __str__(self) -> str:
        return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender    = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    content   = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.sender.username}: {self.content}"