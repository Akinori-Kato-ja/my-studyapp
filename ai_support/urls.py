from django.urls import path
from . import views

app_name = 'ai_support'
urlpatterns = [
    path('generate_learning_topic/<int:draft_id>/', views.generate_learning_topic_view(), name='generate_learning_topic')
]
