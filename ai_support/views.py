from django.shortcuts import render, redirect, get_object_or_404

from task_management.models import DraftLearningGoal


def generate_learning_topic_view(request, draft_id):
    draft = get_object_or_404(
        DraftLearningGoal,
        user=request.user,
        id=draft_id,
    )
