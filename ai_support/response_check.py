import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_common')
django.setup()

from langchain.chains.conversation.base import ConversationChain
from ai_support.ai_chain import get_llm
from ai_support.modules.exam.exam_memory import get_summary_memory
from exam.models import ExamSession, ExamLog, ExamEvaluation
from modules.exam.exam_prompts import get_main_mcq_prompt, get_sub_mcq_prompt
from accounts.models import CustomUser
from task_management.models import Category, UserInterestCategory, LearningGoal, LearningMainTopic, LearningSubTopic
from modules.exam.generate_mcq import generate_mcq
from modules.exam.generate_evaluation import generate_mcq_evaluation


if __name__ == '__main__':
    user, _ = CustomUser.objects.get_or_create(username='luffy')
    category, _ = Category.objects.get_or_create(name='Programming')
    UserInterestCategory.objects.get_or_create(user=user, category=category)

    learning_goal, _ = LearningGoal.objects.get_or_create(
        user=user,
        category=category,
        title='Python',
    )
    main_topic, _ = LearningMainTopic.objects.get_or_create(
        user=user,
        learning_goal=learning_goal,
        main_topic='基礎構文',
    )

    sub_topic, _ = LearningSubTopic.objects.get_or_create(
        user=user,
        learning_goal=learning_goal,
        main_topic=main_topic,
        sub_topic='分岐',
    )
    sub_topic, _ = LearningSubTopic.objects.get_or_create(
        user=user,
        learning_goal=learning_goal,
        main_topic=main_topic,
        sub_topic='ループ処理',
    )
    sub_topic, _ = LearningSubTopic.objects.get_or_create(
        user=user,
        learning_goal=learning_goal,
        main_topic=main_topic,
        sub_topic='関数',
    )

    session, _ = ExamSession.objects.get_or_create(
        user=user,
        main_topic=main_topic,
        format='mcq',
    )

    generate_mcq(session=session)

    exam_log = ExamLog.objects.filter(session=session).order_by('question_number').last()
    print(f'{exam_log.question_number}: {exam_log.question}')
    exam_log.answer = 'B'
    print(f'Answer: {exam_log.answer}')

    generate_mcq_evaluation(exam_log)
