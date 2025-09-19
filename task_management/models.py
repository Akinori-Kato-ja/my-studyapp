from django.db import models



# Category list
class Category(models.Model):
    name = models.CharField(max_length=255)
    is_global = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'accounts.CustomUser',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='own_categories',
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



# Intermediate model (CustomUser, Catogory)
class UserInterestCategory(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'], 
                name='unique_user_interest_category',
                )
        ]
        verbose_name = 'User Interest Category'
        verbose_name_plural = 'User Interest Categories'


# User learning goal
class LearningGoal(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=30, help_text='学習目標(タイトル)を入力してください。(必須)')
    current_level = models.TextField(blank=True, null=True, help_text='現在のレベルを入力してください。(任意)')
    target_level = models.TextField(blank=True, null=True, help_text='学習目標の詳細を入力してください。(任意)')
    target_date = models.DateField(blank=True, null=True, help_text='目標学習期日をカレンダーから選択してください。(任意)')
    total_score = models.FloatField(blank=True, null=True)

    target_study_time = models.FloatField(blank=True, null=True, help_text='目標学習時間(h)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def actual_study_time(self):
        return self.sessions.aggregate(
            total=models.Sum('time_spent')
        )['total'] or 0

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Learning Goal'
        verbose_name_plural = 'Learning Goals'
    

# Learning main topics
class LearningMainTopic(models.Model):
    STATUS = [
        ('incomplete', 'Incomplete'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE)

    main_topic = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='incomplete',
    )

    def __str__(self):
        return self.main_topic
    
    class Meta:
        verbose_name = 'Learning Main Topic'
        verbose_name_plural = 'Learning Main Topics'
    

# Learning sub topics
class LearningSubTopic(models.Model):
    STATUS = [
        ('incomplete', 'Incomplete'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    learning_goal = models.ForeignKey(LearningGoal, on_delete=models.CASCADE)
    main_topic = models.ForeignKey(
        LearningMainTopic, 
        related_name='sub_topics',
        on_delete=models.CASCADE,
    )

    sub_topic = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='incomplete',
    )

    def __str__(self):
        return f'{self.main_topic.main_topic} - {self.sub_topic}'
    
    def save(self, *args, **kwargs):
        if self.main_topic:
            self.learning_goal = self.main_topic.learning_goal
            self.user = self.main_topic.learning_goal.user
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Learning Sub Topic'
        verbose_name_plural = 'Learning Sub Topics'
