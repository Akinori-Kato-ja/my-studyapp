from django.db import models
from django.contrib.auth.models import AbstractUser


# カスタムユーザー(認証情報, 興味分野)
class CustomUser(AbstractUser):
    interest_categories = models.ManyToManyField(
        'task_management.Category',
        through='task_management.UserInterestCategory',
        related_name='interested_users',
    )

    class Meta:
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
