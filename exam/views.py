from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from task_management.models import LearningGoal, LearningMainTopic, LearningSubTopic
from .get_obj import get_topic_matching_url


# Create your views here.
class MultipleChoiceQuizView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Multiple Choice Quiz'

    def get(self, request, topic_id):
        url_name = request.resolver_match.url_name

        if 'main' in url_name:
            topic = get_object_or_404(LearningMainTopic, id=topic_id, user=request.user,)
            title = topic.main_topic

        elif 'sub' in url_name:
            topic = get_object_or_404(LearningSubTopic, id=topic_id, user=request.user,)
            title = topic.sub_topic

        return render(request, self.template_name, {
            'format': self.exam_format,
            'title': title,
        })

class WrittenTaskView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Written Task'
    
    def get(self, request, topic_id):
        url_name = request.resolver_match.url_name

        if 'main' in url_name:
            topic = get_object_or_404(LearningMainTopic, id=topic_id, user=request.user,)
            title = topic.main_topic

        elif 'sub' in url_name:
            topic = get_object_or_404(LearningSubTopic, id=topic_id, user=request.user,)
            title = topic.sub_topic

        return render(request, self.template_name, {
            'format': self.exam_format,
            'title': title,
        })


class ComprehensiveTestView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Comprehensive Test'

    def get(self, request, goal_id):
        goal = get_object_or_404(LearningGoal, id=goal_id, user=request.user)

        return render(request, self.template_name, {
            'format': self.exam_format,
            'title': goal.title,
        })
