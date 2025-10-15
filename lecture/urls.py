from django.urls import path
from lecture import views


app_name='lecture'
urlpatterns = [
    path('lecture/<int:topic_id>/', views.AIGeneratedLectureView.as_view(), name='lecture_generate'),
]
