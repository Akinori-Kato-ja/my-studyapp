import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
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
        if created or not session.logs.exists():
            response = generate_lecture(session=session)
        else:
            # Second time onwards
            summary = session.summary if session.summary else 'The content of the previous lecture could not be retrieved.'
            last_ai_log = session.logs.filter(role='ai').last()
            response = last_ai_log.message if last_ai_log else 'No lecture yet.'

        print(f'Type(response): {type(response)}')
        html_response = mark_safe(markdown.markdown(response))


        return render(request, self.template_name, {
            'session': session,
            'logs': session.logs.all(),
            'response': html_response,
            'summary': summary,
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

        return render(request, self.template_name, {
            'session': session,
            'logs': session.logs.all(),
            'response': html_response,
        })
