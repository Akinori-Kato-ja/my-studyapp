from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import AddInterestCategoryForm, SettingLearningGoalForm
from .models import UserInterestCategory, DraftLearningGoal, LearningGoal
from accounts.models import CustomUser


# === Top page ===
class IndexView(generic.TemplateView):
    template_name = 'task_management/index.html'


# === Interest category === 
# List page
class InterestCategoryListView(LoginRequiredMixin, generic.ListView):
    model = UserInterestCategory
    template_name = 'task_management/interest_categories.html'
    context_object_name = 'interest_categories'

    def get_queryset(self):
        return UserInterestCategory.objects.filter(user=self.request.user)


# Add
class AddInterestCategoryView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'task_management/add_interest_category.html'
    success_url = reverse_lazy('task_management:interest_categories')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

# Delete
class DeleteInterestCategoryView(LoginRequiredMixin, generic.DeleteView):
    model = UserInterestCategory
    template_name = 'task_management/delete_interest_category.html'
    success_url = reverse_lazy('task_management:interest_categories')


# === Learning goal === 
# List page
class LearningGoalListView(LoginRequiredMixin, generic.ListView):
    model = LearningGoal
    template_name = 'task_management/learning_goal_list.html'
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
    

# Setting
class SettingLearningGoalView(generic.CreateView):
    model = DraftLearningGoal
    form_class = SettingLearningGoalForm
    template_name = 'task_management/setting_learning_goal.html'
    success_url = reverse_lazy('#')

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
        draft.category = get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            id=self.kwargs['user_interest_id']
        )
        draft.save()
        return redirect('')

    
