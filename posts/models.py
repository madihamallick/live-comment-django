from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()
class Premise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text =  models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    premise = models.ForeignKey(
        Premise, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    text = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class ReplyOnComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter_reply")
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_replies')
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
