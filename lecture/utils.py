from django.db.models import Sum
from .models import LectureLog


# Get the total token usage for the entire learning objective
def get_total_tokens_for_goal(learning_goal):
    return (
        LectureLog.objects
        .filter(session__sub_topic__learning_goal=learning_goal)
        .aaggregate(total=Sum('token_count'))['total'] or 0
    )
