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
    # Must be linked to a learning goal, main topic, or subtopic
    learning_goal = models.ForeignKey(
        'task_management.LearningGoal',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='exams_goal',
    )
    main_topic = models.ForeignKey(
        'task_management.LearningMainTopic',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='exams_main',
    )
    sub_topic = models.ForeignKey(
        'task_management.LearningSubTopic',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='exams_sub',
    )

    current_question_number = models.IntegerField(default=0)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    summary = models.TextField(blank=True)
    used_tokens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.format in ('mcq', 'wt'):
            if bool(self.main_topic) == bool(self.sub_topic):
                raise ValidationError('Please specify either main_topic or sub_topic, not both.')
        elif self.format == 'ct':
            if not self.learning_goal or self.main_topic or self.sub_topic:
                raise ValidationError('CT must be linked only to a learning goal.')

    def recalculation_used_tokens(self):
        """Recalculate total token usage based on all related ExamLogs."""
        total = self.logs.aggregate(total_tokens=models.Sum('token_count'))['total_tokens'] or 0
        self.used_tokens = total
        self.save(update_fields=['used_tokens'])

    def __str__(self):
        if self.learning_goal:
            return f'{self.learning_goal.title} - {self.format}'
        elif self.main_topic:
            return f'{self.main_topic.main_topic} - {self.format}'
        elif self.sub_topic:
            return f'{self.sub_topic.sub_topic} - {self.format}'
        return f'Exam: (no topic)'


class ExamLog(models.Model):
    session = models.ForeignKey(
        ExamSession,
        on_delete=models.CASCADE,
        related_name='logs',
    )
    question_number = models.IntegerField(default=0)
    question = models.TextField()
    answer = models.TextField(blank=True)
    token_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'question_number'],
                name='unique_session_question_number'
            ),
        ]

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
        return f'Log: {self.session.user} - {self.session} - No.{self.question_number}'


class ExamEvaluation(models.Model):
    exam_log = models.OneToOneField(
        ExamLog,
        on_delete=models.CASCADE,
        related_name='evaluation',
    )
    score = models.FloatField()
    feedback = models.TextField()
    token_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Evaluation for {self.exam_log}(score:{self.score})'
