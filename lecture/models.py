from django.db import models
from config import settings_common


# Create your models here.
class LectureSession(models.Model):
    user = models.ForeignKey(settings_common.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_topic = models.ForeignKey('task_management.LearningSubTopic', on_delete=models.CASCADE)
    summary = models.TextField(blank=True)
    total_tokens = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.sub_topic.sub_topic}'
    

class LectureLog(models.Model):
    ROLE_CHOICES = [
        ('ai', 'AI'),
        ('user', 'USER'),
        ('master', 'MASTER'),
    ]

    session = models.ForeignKey(LectureSession, on_delete=models.CASCADE, related_name='logs')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    token_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.role}: {self.message[:30]}'
