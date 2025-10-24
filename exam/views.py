from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from task_management.models import LearningMainTopic, LearningSubTopic


# Create your views here.
class MultipleChoiceQuizView(LoginRequiredMixin, View):
    pass


class WrittenTaskView(LoginRequiredMixin, View):
    pass


class ComprehensiveTestView(LoginRequiredMixin, View):
    pass
