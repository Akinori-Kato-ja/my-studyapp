from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views import generic, View
from ai_support.modules.exam import generate_mcq
from task_management.models import LearningGoal, LearningMainTopic, LearningSubTopic
from .models import ExamSession, ExamLog, ExamEvaluation


# Multiple Choice Quiz
class MultipleChoiceQuizView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Multiple Choice Quiz'

    def get(self, request, topic_id, question_number):
        url_name = request.resolver_match.url_name

        if 'main' in url_name:
            topic = get_object_or_404(LearningMainTopic, id=topic_id, user=self.request.user)
            session, created = ExamSession.objects.get_or_create(
                user=self.request.user,
                main_topic=topic,
                format='mcq',
            )
            title = topic.main_topic
        elif 'sub' in url_name:
            topic = get_object_or_404(LearningSubTopic, id=topic_id, user=self.request.user)
            session, created = ExamSession.objects.get_or_create(
                user=self.request.user,
                sub_topic=topic,
                format='mcq',
            )
            title = topic.sub_topic

        if created or not session.logs.exists():
            question = generate_mcq(session=session)
        else:
            last_log = session.logs.last()
            question = last_log.question if last_log else 'No logs.'
        if not question:
            context = {'message': 'Problem generation failed, please try again.'}
            return render(request, 'exam/exam_error.html', context)


        return render(request, self.template_name, {
            'format': self.exam_format,
            'title': title,
            'question': question,
        })
    
    def post(self, request, topic_id):
        url_name = request.resolver_match.url_name

        # 


# Written Task
class WrittenTaskView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Written Task'
    
    def get(self, request, topic_id, question_number):
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


# Comprehensive Test (All topics)
class ComprehensiveTestView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    exam_format = 'Comprehensive Test'

    def get(self, request, goal_id):
        goal = get_object_or_404(LearningGoal, id=goal_id, user=request.user)

        return render(request, self.template_name, {
            'format': self.exam_format,
            'title': goal.title,
        })
