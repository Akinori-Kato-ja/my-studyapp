from django.db import models
from django.utils import timezone
from config import settings_common


# Save user learning records(Raw Data)
class StudySession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('lec', 'Lecture'),
        ('mcq', 'Multiple Choice Quiz'),
        ('wt', 'Written Task'),
        ('ct', 'Comprehensive Test'),
        ('review', 'Review'),
    ]

    user = models.ForeignKey(settings_common.AUTH_USER_MODEL, related_name='sessions', on_delete=models.CASCADE)
    learning_goal = models.ForeignKey(
        'task_management.LearningGoal',
        on_delete=models.CASCADE,
        related_name='sessions',
        null=True,
        blank=True,
        )
    score = models.FloatField(blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_spent = models.FloatField(blank=True, null=True, help_text='Study time in hours')
    session_type = models.CharField(
        max_length=30,
        choices=SESSION_TYPE_CHOICES,
    )

    class Meta:
        verbose_name = 'Study Session'
        verbose_name_plural = 'Study Sessions'
    
    def save(self, *args, **kwargs):
        if self.end_time and self.start_time:
            start = timezone.make_aware(self.start_time) if timezone.is_naive(self.start_time) else self.start_time
            end = timezone.make_aware(self.end_time) if timezone.is_naive(self.end_time) else self.end_time

            duration = end - start
            self.time_spent = round(duration.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} | {self.session_type} | {self.start_time:%Y-%m-%d %H:%M}'
    
