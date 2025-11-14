import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic, View
from django.urls import reverse
from django.utils.safestring import mark_safe
from ai_support.modules.lecture.generate_lecture import generate_lecture
from task_management.models import LearningMainTopic, LearningSubTopic
from .models import LectureSession, LectureLog


# Create your views here.
class LectureView(LoginRequiredMixin, View):
    template_name = 'lecture/lecture.html'

    def get(self, request, topic_id):
        sub_topic = get_object_or_404(
            LearningSubTopic,
            id=topic_id,
            user=self.request.user,
        )
        
        session, created = LectureSession.objects.get_or_create(
            user=request.user,
            sub_topic=sub_topic,
        )

        summary = None
        # Generate the first lecture

        if created:
            session.lecture_count = 1
            response = generate_lecture(session=session)
        else:
            # Second time onwards
            session.lecture_count += 1
            response = generate_lecture(session=session)

        print(f'Type(response): {type(response)}')
        html_response = mark_safe(markdown.markdown(response))


        return render(request, self.template_name, {
            'session': session,
            'first_response': html_response,
        })
        
    def post(self, request, topic_id):
        sub_topic = get_object_or_404(
            LearningSubTopic,
            id=topic_id,
            user=self.request.user,
        )
        session = get_object_or_404(
            LectureSession,
            user=request.user,
            sub_topic=sub_topic,
        )

        user_input = request.POST.get('user_input', '').strip()
        response = generate_lecture(session=session, user_input=user_input)

        html_response = mark_safe(markdown.markdown(response))


        return JsonResponse({'next_response': html_response})
