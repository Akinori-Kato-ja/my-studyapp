from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View
from django.urls import reverse
from task_management.models import LearningMainTopic, LearningSubTopic


# Create your views here.
class LectureView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(
            LearningSubTopic,
            id=self.kwargs['topic_id'],
            user=self.request.user,
        )
        
        context = {
            'topic': topic,
        }

        return render(request, 'lecture/lecture.html', context)
