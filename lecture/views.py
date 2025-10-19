from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View
from django.urls import reverse
from task_management.models import LearningMainTopic, LearningSubTopic


# Create your views here.
class GenerateLectureView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pass
