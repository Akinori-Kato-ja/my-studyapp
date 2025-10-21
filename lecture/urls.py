from django.urls import path
from lecture import views


app_name='lecture'
urlpatterns = [
    path('<int:topic_id>/', views.LectureView.as_view(), name='lecture'),
]
