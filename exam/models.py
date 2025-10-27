from django.db import models, transaction
from django.core.exceptions import ValidationError
from config import settings_common


# Create your models here.
class ExamSession(models.Model):
    FORMAT_CHOICES = [
        ('mcq', 'MCQ'),  # Multiple Choice Quiz
        ('wt', 'WT'),  # Written Task
        ('ct', 'CT'),  # Conprehensive Test
    ]

    user = models.ForeignKey(settings_common.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Must be linked to a learning objective, main topic, or subtopic
    learning_goal = models.ForeignKey(
        'task_management.LearningGoal',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='exams_goal',
    )
    main_topic = models.ForeignKey(
        'task_management.LearningMainTopic',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='exams_main'
    )
    sub_topic = models.ForeignKey(
        'task_management.LearningSubTopic',
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='exams_sub',
    )
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    total_tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.format == 'mcq' or self.format == 'wt':
            if not self.main_topic and not self.sub_topic:
                raise ValidationError('Please specify either main_topic or sub_topic.')
            if self.main_topic and self.sub_topic:
                raise ValidationError('main_topic and sub_topic cannot be set at the same time.')
        if self.format == 'ct':
            if not self.learning_goal:
                raise ValidationError('Comprehensive tests should be linked to learning goals.')
            if self.main_topic or self.sub_topic:
                raise ValidationError('Comprehensive tests cannot be linked to topics.')

    def __str__(self):
        if self.learning_goal:
            return f'Exam: {self.user} - {self.learning_goal.title} - {self.format}'
        elif self.main_topic:
            return f'Exam: {self.user} - {self.main_topic.main_topic} - {self.format}'
        elif self.sub_topic:
            return f'Exam: {self.user} - {self.sub_topic.sub_topic} - {self.format}'
        return f'Exam: (no topic)'


class ExamLog(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    question = models.TextField()
    answer = models.TextField()
    token_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'question_number') 

    def save(self, *args, **kwargs):
        if not self.pk:
            with transaction.atomic():
                last_number = (
                    ExamLog.objects
                    .select_for_update()
                    .filter(session=self.session)
                    .aggregate(models.Max('question_number'))['question_number__max'] or 0
                )
                self.question_number = last_number + 1
        super().save(*args, **kwargs)

    def __str__(self):
        if self.session.learning_goal:
            return f'Exam log: {self.session.user} - {self.session.learning_goal.title} - {self.session.format}'
        elif self.session.main_topic:
            return f'Exam log: {self.session.user} - {self.session.main_topic.main_topic} - {self.session.format}'
        elif self.session.sub_topic:
            return f'Exam log: {self.session.user} - {self.session.sub_topic.sub_topic} - {self.session.format}'
        return f'Exam log: {self.session.user} - {self.session.format}'
