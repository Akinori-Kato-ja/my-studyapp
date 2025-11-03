from django.urls import path
from . import views


app_name = 'exam'
urlpatterns = [
    # Multiple Choice Quiz
    path('<int:topic_id>/mcq/main/<int:question_number>/', views.MultipleChoiceQuizView.as_view(), name='exam_mcq_main'),
    path('<int:topic_id>/mcq/sub/<int:question_number>/', views.MultipleChoiceQuizView.as_view(), name='exam_mcq_sub'),
    # Written Task
    path('<int:topic_id>/wt/main/<int:question_number>/', views.WrittenTaskView.as_view(), name='exam_wt_main'),
    path('<int:topic_id>/wt/sub/<int:question_number>/', views.WrittenTaskView.as_view(), name='exam_wt_sub'),
    # Conprehensive Test
    path('<int:goal_id>/ct/<int:question_number>/', views.ComprehensiveTestView.as_view(), name='exam_ct'),
]
