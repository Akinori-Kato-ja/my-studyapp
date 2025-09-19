from django import forms

from .models import UserInterestCategory, LearningGoal


# Add Interest Category
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
