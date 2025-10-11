from django.shortcuts import render, redirect, get_object_or_404

from ai_support.ai_services import generate_learning_topic
from task_management.models import DraftLearningGoal


def generate_learning_topic_view(request, draft_id):
    draft = get_object_or_404(
        DraftLearningGoal,
        user=request.user,
        id=draft_id,
    )

    # AI generation
    generated = generate_learning_topic(
        title=draft.title,
        current_level=draft.current_level,
        target_level=draft.target_level,
    )

    # Save to DraftLearningGoal
    draft.raw_generated_data = generated
    draft.save()

    return redirect('task_management:preview_generated_learning_topic', draft_id=draft.id)

