from django.urls import path
from . import views


app_name = 'exam'
urlpatterns = [
    path('<int:topic_id>/mcq/', views.MultipleChoiceQuizView.as_view(), name='exam_mcq'),
    path('<int:topic_id>/wt/', views.WrittenTaskView.as_view(), name='exam_wt'),
    path('<int:topic_id>/ct/', views.ComprehensiveTestView.as_view(), name='exam_ct'),
]
