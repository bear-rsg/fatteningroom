from django import forms
from . import models


class QuestionnaireCreateForm(forms.ModelForm):
    """
    A form for users to create a new 'Questionnaire' object
    """

    class Meta:
        model = models.Questionnaire
        fields = [
            'story_text',
            'story_file',
            'permission_contact',
            'email',
            'permission_public',
            'age',
            'gender',
            'ethnicity',
            'country_of_residence'
        ]

        # Adding labels and widgets to make the form user-friendly
        labels = {
            'story_text': 'Share your story here',
            'story_file': 'Upload an image or audio file to support your story (optional, file size limit 20MB)',
            'permission_contact': 'I am happy to be contacted by the project team about my feedback (optional)',
            'permission_public': 'I am happy for my feedback to be made public (optional)',
            'email': 'Email (provide if happy to be contacted, otherwise optional)',
            'age': 'Age (optional)',
            'gender': 'Gender (optional)',
            'ethnicity': 'Ethnicity (optional)',
            'country_of_residence': 'Country of residence (optional)',
        }

        widgets = {
            'story_text': forms.Textarea(attrs={
                'rows': 8,
                'placeholder': 'Tell us your story...',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@example.com',
                'class': 'form-control',
                'required': False
            }),
            'age': forms.Select(attrs={'class': 'form-select'}),
        }
