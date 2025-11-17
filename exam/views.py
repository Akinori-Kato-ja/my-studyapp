import json
import markdown
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.views import generic, View
from ai_support.modules.exam.generate_mcq import generate_mcq
from ai_support.modules.exam.generate_evaluation import generate_mcq_evaluation
from task_management.models import LearningGoal, LearningMainTopic, LearningSubTopic
from .models import ExamSession, ExamLog, ExamEvaluation


# Multiple Choice Quiz
class MultipleChoiceQuizView(LoginRequiredMixin, View):
    template_name = 'exam/exam.html'
    format_text = 'Multiple Choice Quiz'

    def get(self, request, topic_id):
        url_name = request.resolver_match.url_name
        full_url_name = f'exam:{url_name}'

        if 'main' in url_name:
            topic_obj = get_object_or_404(LearningMainTopic, id=topic_id, user=request.user)
            topic_filter = {'main_topic': topic_obj}

        elif 'sub' in url_name:
            topic_obj = get_object_or_404(LearningSubTopic, id=topic_id, user=request.user)
            topic_filter = {'sub_topic': topic_obj}

        else:
            raise ValueError('The URL name does not contain "main" or "sub".')
        
        last_session = (
            ExamSession.objects
            .filter(user=request.user, format='mcq', **topic_filter)
            .order_by('-attempt_number')
            .first()
        )

        attempt_number = last_session.attempt_number + 1 if last_session else 1

        # create session
        session = ExamSession.objects.create(
            user=request.user,
            format='mcq',
            attempt_number=attempt_number,
            **topic_filter,
        )

        # Manage test data with a unique attempt_number
        request.session['attempt_number'] = attempt_number

        # Generate Multiple Choice Quiz
        question_number, question = generate_mcq(session=session)
        
        if not question:
            context = {'message': 'Problem generation failed, please try again.'}
            return render(request, 'exam/exam_error.html', context)

        html_question = mark_safe(markdown.markdown(question))

        context = {
            # for display
            'format': self.format_text,  
            'topic': topic_obj,
            # generated
            'first_question_number': question_number,
            'first_question_html': html_question,
            # used in URL parameters
            'url_name': full_url_name, 
        }

        return render(request, self.template_name, context)
    
    def post(self, request, topic_id):
        url_name = request.resolver_match.url_name
        full_url_name = f'exam:{url_name}'

        data = json.loads(request.body)
        answer = data.get('user_input')

        attempt_number = request.session.get('attempt_number')

        if 'main' in url_name:
            topic_obj = get_object_or_404(LearningMainTopic, id=topic_id, user=self.request.user)
            topic_filter = {'main_topic': topic_obj}

        elif 'sub' in url_name:
            topic_obj = get_object_or_404(LearningSubTopic, id=topic_id, user=self.request.user)
            topic_filter = {'sub_topic': topic_obj}
        else:
            raise ValueError('The URL name does not contain "main" or "sub".')

        session = get_object_or_404(
            ExamSession,
            user=self.request.user,
            format='mcq',
            attempt_number=attempt_number,
            **topic_filter,
        )

        current_question_number = session.current_question_number

        try:
            exam_log = ExamLog.objects.get(
                session=session,
                question_number=current_question_number,
            )
        except ExamLog.DoesNotExist:
            print('There is no corresponding log.')
            score, explanation = 0, 'A problem has occurred.'
        except ExamLog.MultipleObjectsReturned:
            print('There are multiple logs that match the conditions.')
            score, explanation = 0, 'A problem has occurred.'
        else:
            exam_log.answer = answer
            # generate evaluation
            score, explanation = generate_mcq_evaluation(log=exam_log)
            html_explanation = mark_safe(markdown.markdown(explanation))

        print(f'score: {score}')
        print(f'explanation: {explanation}')

        response_data = {
            # for display
            'format': self.format_text,
            'topic': topic_obj,
            # generated data
            'score': score,
            'explanation': html_explanation,
            # used in URL parameters
            'url_name': full_url_name,
        }

        if current_question_number <= 5:
            # generate next question
            question_number, question = generate_mcq(session=session)
            if not question:
                context = {'message': 'Problem generation failed, please try again.'}
                return render(request, 'exam/exam_error.html', context)

            html_question = mark_safe(markdown.markdown(question))

            response_data.update({
                # generated data
                'next_question_number': question_number,
                'next_question': html_question,
            })

        else:
            total_token = total_score = 0
            for log in session.logs.all():
                total_token += log.token_count
                total_score += log.evaluation.score
            
            session.used_tokens = total_token
            session.total_score = total_score

            response_data.update({
                'total_score': total_score
            })
        
        return JsonResponse(response_data)


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
