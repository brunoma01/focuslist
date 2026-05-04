from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['label', 'due_date']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

def clean_first_name(self):
    name = self.cleaned_data.get('first_name')
    return name.capitalize()

def save(self, commit=True):
    user = super().save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    if commit:
        user.save()
    return user