from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from django import forms

from .models import UserInterestCategory, LearningGoal


# Add: Interest Category
class AddInterestCategoryForm(forms.ModelForm):
    class Meta:
        model = UserInterestCategory
        fields = ['category']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'category': 'Select the category you want to add'
        }


# Setting: Learning Goal
class SettingLearningGoalForm(forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ['title', 'current_level', 'target_level']
        labels = {
            'title': 'Title *',
            'current_level': 'Current level (optional)',
            'target_level': 'Target level (optional)',
        }
        # help_texts = {
        #     'title': 'Enter your learning goal title. (Required)',
        #     'current_level': 'Describe your current skill level. (Optional)',
        #     'target_level': 'Describe your ultimate learning goal in detail. (Optional)',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Field(
                "title",
                css_class="form-control",
                placeholder="Enter a title (e.g., Python Stock Price Prediction)"
            ),
            Field(
                "current_level",
                css_class="form-control",
                rows="3",
                placeholder="Describe your current learning status (e.g., I have mastered basic Python grammar)"
            ),
            Field(
                "target_level",
                css_class="form-control",
                rows="5",
                placeholder=(
                    "Describe your ultimate learning goal. "
                    "(e.g., I want to create a stock price prediction program in Python "
                    "and use it in actual stock trading.) "
                    "* The more details you provide, the better the generated tasks will be."
                )
            ),
            Div(
                Submit("submit", "Send", css_class="btn btn-primary"),
                css_class="mb-4"
            ),
        )
