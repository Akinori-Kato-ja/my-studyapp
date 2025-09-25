from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import AddInterestCategoryForm
from .models import UserInterestCategory, LearningGoal
from accounts.models import CustomUser


# Top page
class IndexView(generic.TemplateView):
    template_name = 'task_management/index.html'


# List: Interest Category
class InterestCategoryListView(LoginRequiredMixin, generic.ListView):
    model = UserInterestCategory
    template_name = 'task_management/interest_categories.html'
    context_object_name = 'interest_categories'

    def get_queryset(self):
        return UserInterestCategory.objects.filter(user=self.request.user)


# Add: Interest Category
class AddInterestCategoryView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'task_management/add_interest_category.html'
    success_url = reverse_lazy('task_management:interest_categories')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

# Delete: Interest Category
class DeleteInterestCategoryView(LoginRequiredMixin, generic.DeleteView):
    model = UserInterestCategory
    template_name = 'task_management/delete_interest_category.html'
    success_url = reverse_lazy('task_management:interest_categories')


# List: Learning Goal
class LearningGoalListView(LoginRequiredMixin, generic.ListView):
    model = LearningGoal
    template_name = 'task_management/learning_goal_list.html'
    context_object_name = 'learning_goals'

    def get_queryset(self):
        cateogy_id = self.kwargs['category_id']
        return LearningGoal.objects.filter(
            user=self.request.user,
            category_id=cateogy_id,
        )

