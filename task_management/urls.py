from django.urls import path
from task_management import views

app_name = 'task_management'
urlpatterns = [
    # Top page
    path('', views.IndexView.as_view(), name='index'),
    # Interest Category
    path('interest_categories/', views.InterestCategoryListView.as_view(), name='interest_list'),
    path('interest_category/add/', views.AddInterestCategoryView.as_view(), name='interest_add'),
    path('interest_category/<int:pk>/delete/', views.DeleteInterestCategoryView.as_view(), name='interest_delete'),
    # Learning Goal
    path('learning_goals/<int:user_interest_id>', views.LearningGoalListView.as_view(), name='goal_list'),
    path('learning_goal/<int:user_interest_id>/set/', views.SettingLearningGoalView.as_view(), name='goal_set'),
    path('learning_goal/<int:draft_id>/preview/', views.PreviewGeneratedLearningTopicView.as_view(), name='goal_preview'),
    path('learning_goal/<int:draft_id>/finalize/', views.FinalizeLearningGoalView.as_view(), name='goal_finalize'),
]
