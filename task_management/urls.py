from django.urls import path
from task_management import views

app_name = 'task_management'
urlpatterns = [
    # Top page
    path('', views.IndexView.as_view(), name='index'),
    # Interest Category
    path('interest-categories/', views.InterestCategoryListView.as_view(), name='interest_list'),
    path('interest-category/add/', views.InterestCategoryCreateView.as_view(), name='interest_add'),
    path('interest-category/<int:pk>/delete/', views.InterestCategoryDeleteView.as_view(), name='interest_delete'),
    # Learning Goal
    path('learning-goals/<int:user_interest_id>', views.LearningGoalListView.as_view(), name='goal_list'),
    path('learning-goal/<int:user_interest_id>/set/', views.LearningGoalCreateView.as_view(), name='goal_set'),
    path('learning-goal/<int:draft_id>/preview/', views.LearningTopicPreviewView.as_view(), name='goal_preview'),
    path('learning-goal/<int:draft_id>/finalize/', views.LearningGoalFinalizeView.as_view(), name='goal_finalize'),
    path('learning_goal/<int:goal_id>/detail/', views.LearningGoalDetailView.as_view(), name='goal_detail'),
    path('learning_goal/<int:pk>/delete/', views.LearningGoalDeleteView.as_view(), name='goal_delete'),
]
