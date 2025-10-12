from django.urls import path
from . import views

app_name = 'ai_support'
urlpatterns = [
    path('learning-goal/<int:draft_id>/generate-topic/', views.learning_topic_generate_view, name='topic_generate')
]
