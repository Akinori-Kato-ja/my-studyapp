from django.urls import path
from . import views


app_name = 'exam'
urlpatterns = [
    # Multiple Choice Quiz
    path('<int:topic_id>/mcq/main/', views.MultipleChoiceQuizView.as_view(), name='exam_mcq_main'),
    path('<int:topic_id>/mcq/sub/', views.MultipleChoiceQuizView.as_view(), name='exam_mcq_sub'),
    # Written Task
    path('<int:topic_id>/wt/main/', views.WrittenTaskView.as_view(), name='exam_wt_main'),
    path('<int:topic_id>/wt/sub/', views.WrittenTaskView.as_view(), name='exam_wt_sub'),
    # Comprehensive Test
    path('<int:goal_id>/ct/', views.ComprehensiveTestView.as_view(), name='exam_ct'),
]
