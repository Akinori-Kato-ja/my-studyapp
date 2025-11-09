from django.db import models
from config import settings_common


# Save user learning records(Raw Data)
class StudySession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('comprehensive_test', 'COMPREHENSIVE TEST'),
        ('main_topic_test', 'MAIN-TOPIC TEST'),
        ('sub_topic_test', 'SUB-TOPIC TEST'),
        ('review', 'REVIEW')
    ]

    user = models.ForeignKey(settings_common.AUTH_USER_MODEL, related_name='sessions', on_delete=models.CASCADE)
    exam_session = models.ForeignKey('exam.ExamSession', on_delete=models.CASCADE, related_name='study_sessions')
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
