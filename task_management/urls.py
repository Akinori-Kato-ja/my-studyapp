from django.urls import path
from task_management import views

app_name = 'task_management'
urlpatterns = [
    # Top page
    path('', views.IndexView.as_view(), name='index'),
    # Interest Category
    path('interest_categories/', views.InterestCategoryListView.as_view(), name='interest_categories'),
    path('interest_category/add/', views.AddInterestCategoryView.as_view(), name='add_interest_category'),
    path('interest_category/<int:pk>/delete/', views.DeleteInterestCategoryView.as_view(), name='delete_interest_category'),
    # Learning Goal
    path('learning_goals/<int:user_interest_id>', views.LearningGoalListView.as_view(), name='learning_goals'),
    path('learning_goal/<int:user_interest_id>/set/', views.SettingLearningGoalView.as_view(), name='setting_learning_goal'),
    path('learning_goal/<int:draft_id>/preview/', views.PreviewGeneratedLearningTopicView.as_view(), name='preview_generated_learning_topic'),
    path('learning_goal/<int:draft_id>/finalize/', views.FianalizeLearningGoalView.as_view(), name='learning_goal_finalize'),
]
