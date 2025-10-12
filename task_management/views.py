import json
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import AddInterestCategoryForm, SettingLearningGoalForm
from .models import (
    UserInterestCategory,
    DraftLearningGoal,
    LearningGoal,
    LearningMainTopic,
    LearningSubTopic,
)
from accounts.models import CustomUser


# ===== Top page =====
class IndexView(generic.TemplateView):
    template_name = 'task_management/index.html'


# ===== Interest category =====
# List
class InterestCategoryListView(LoginRequiredMixin, generic.ListView):
    model = UserInterestCategory
    template_name = 'task_management/interest_category/list.html'
    context_object_name = 'interest_categories'

    def get_queryset(self):
        return UserInterestCategory.objects.filter(user=self.request.user)


# Create (User Selection)
class InterestCategoryCreateView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'task_management/interest_category/add.html'
    success_url = reverse_lazy('task_management:interest_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

# Delete
class InterestCategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserInterestCategory
    template_name = 'task_management/interest_category/delete.html'
    success_url = reverse_lazy('task_management:interest_list')


# ===== Learning goal =====
# List 
class LearningGoalListView(LoginRequiredMixin, generic.ListView):
    model = LearningGoal
    template_name = 'task_management/learning_goal/list.html'
    context_object_name = 'learning_goals'

    def get_queryset(self):
        user_interest = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            id=self.kwargs['user_interest_id'],
        )
        
        return LearningGoal.objects.filter(
            user=self.request.user,
            category=user_interest.category,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_interest = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            id=self.kwargs['user_interest_id']
        )
        context["category"] = user_interest.category
        context['user_interest'] = user_interest
        return context
    

# Create (User Input)
class LearningGoalCreateView(LoginRequiredMixin, generic.CreateView):
    model = DraftLearningGoal
    form_class = SettingLearningGoalForm
    template_name = 'task_management/learning_goal/setting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_interest = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            id=self.kwargs['user_interest_id']
        )
        context['user_interest'] = user_interest
        return context

    def form_valid(self, form):
        draft = form.save(commit=False)
        draft.user = self.request.user
        user_interest = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            id=self.kwargs['user_interest_id']
        )
        draft.category = user_interest.category
        draft.save()
        return redirect('ai_support:topic_generate', draft_id=draft.id)


# Preview (Generated Topic)
class LearningTopicPreviewView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task_management/learning_goal/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = get_object_or_404(
            DraftLearningGoal,
            user=self.request.user,
            id=self.kwargs['draft_id']
        )

        user_interest = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            category=draft.category
        )

        if isinstance(draft.raw_generated_data, list):
            topics_data = draft.raw_generated_data
        elif isinstance(draft.raw_generated_data, str):
            try:
                topics_data = json.loads(draft.raw_generated_data)
            except json.JSONDecodeError:
                topics_data = []
        else:
            topics_data = []

        context["draft"] = draft
        context['user_interest'] = user_interest
        context["topics"] = topics_data
        return context


# Finalize (LearningGoal and LearningTopics)
class LearningGoalFinalizeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        draft = get_object_or_404(
            DraftLearningGoal,
            user=request.user,
            id=self.kwargs['draft_id']
        )

        # Load the original generated data
        if isinstance(draft.raw_generated_data, list):
            topics_data = draft.raw_generated_data
        elif isinstance(draft.raw_generated_data, str):
            try:
                topics_data = json.loads(draft.raw_generated_data)
            except json.JSONDecodeError:
                messages.error(request, 'Generated data is invalid.')
                return redirect('task_management:goal_preview', draft_id=draft.id)

        # Get selected main_topics
        selected_main_topics = request.POST.getlist('main_topics')

        # Save learning goal
        learning_goal = LearningGoal.objects.create(
            user=self.request.user,
            category=draft.category,
            draft=draft,
            title=draft.title,
            current_level=draft.current_level,
            target_level=draft.target_level,
        )

        # Save checked main_topics
        for topic in topics_data:
            if topic['main_topic'] not in selected_main_topics:
                continue

            main_topic = LearningMainTopic.objects.create(
                user=request.user,
                learning_goal=learning_goal,
                main_topic=topic['main_topic'],
            )

            # Get Selected sub_topics
            sub_topic_key = f'{topic["main_topic"]}_sub_topics'
            selected_sub_topics = request.POST.getlist(sub_topic_key)

            # Save checked sub_topics
            for sub in topic['sub_topics']:
                if sub['sub_topic'] not in selected_sub_topics:
                    continue

                LearningSubTopic.objects.create(
                    user=request.user,
                    learning_goal=learning_goal,
                    main_topic=main_topic,
                    sub_topic=sub['sub_topic']
                )

        draft.is_finalized = True
        draft.save()

        messages.success(request, 'Learning goal has been successfully saved!')
        return redirect('task_management:goal_detail', goal_id=learning_goal.id)
    

# Detail
class LearningGoalDetailView(LoginRequiredMixin, generic.DetailView):
    model = LearningGoal
    template_name = 'task_management/learning_goal/detail.html'
    context_object_name = 'goal'
    pk_url_kwarg = 'goal_id'

    def get_object(self, queryset=None):
        return get_object_or_404(
            LearningGoal,
            id=self.kwargs['goal_id'],
            user=self.request.user,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.get_object()

        # Get main-topics and sub-topics at the same time
        main_topics = LearningMainTopic.objects.filter(
            learning_goal=goal,
        ).prefetch_related('sub_topics')

        context["main_topics"] = main_topics
        return context
