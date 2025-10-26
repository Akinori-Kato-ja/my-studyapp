from django.shortcuts import get_object_or_404
from task_management.models import (
    LearningGoal,
    LearningMainTopic,
    LearningSubTopic,
)

def get_topic_matching_url(user, id, url_name: str):
    topic = None
    if 'main' in url_name:
        topic = get_object_or_404(
            LearningMainTopic,
            id=id,
            user=user,
        )
        topic_title = topic.main_topic

    elif 'sub' in url_name:
        topic = get_object_or_404(
            LearningSubTopic,
            id=id,
            user=user,
        )
        topic_title = topic.sub_topic

    return topic, topic_title