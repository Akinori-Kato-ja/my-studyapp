from django.db import models


# Save user learning records(Raw Data)
class StudySession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('comprehensive_test', 'COMPREHENSIVE TEST'),
        ('main_topic_test', 'MAIN-TOPIC TEST'),
        ('sub_topic_test', 'SUB-TOPIC TEST'),
        ('review', 'REVIEW')
    ]

    user = models.ForeignKey(
        'accounts.CustomUser',
        related_name='sessions',
        on_delete=models.CASCADE,
    )
    learning_goal = models.ForeignKey(
        'task_management.LearningGoal',
        related_name='sessions',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    main_topic = models.ForeignKey(
        'task_management.LearningMainTopic',
        related_name='sessions',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )
    sub_topic = models.ForeignKey(
        'task_management.LearningSubTopic',
        related_name='sessions',
        blank=True, null=True,
        on_delete=models.CASCADE,
    )

    score = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    time_spent = models.FloatField(blank=True, null=True, help_text='Study time in this session.(hours)')
    session_type = models.CharField(
        max_length=30,
        choices=SESSION_TYPE_CHOICES,
        default='sub_topic_test',
    )

    def __str__(self):
        return f'{self.user} | {self.session_type} | {self.date:%Y-%m-%d %H:%M}'
    
    class Meta:
        verbose_name = 'Study Session'
        verbose_name_plural = 'Study Sessions'
